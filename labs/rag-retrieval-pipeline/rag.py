"""The retrieval-augmented generation (RAG) loop that frameworks like LangChain package up.

1. Load documents and split them into overlapping chunks that keep their source.
2. Index the chunks (TF-IDF here; an embedding model + vector store in production).
3. Retrieve the top-k chunks for a question.
4. Build a prompt that tells the model to answer only from those chunks and cite them.
5. Call the model (any provider) and refuse when retrieval found nothing relevant.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

STOP = set("a an and are as at be by can for from in is it its may must not of on or the to this was what when which with".split())


@dataclass(frozen=True)
class Chunk:
    source: str
    section: str
    text: str


def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]


def load_chunks(folder: Path, max_words: int = 60, overlap: int = 15) -> list[Chunk]:
    chunks = []
    for path in sorted(folder.glob("*.md")):
        section = path.stem
        for block in path.read_text().split("\n## "):
            lines = block.strip().splitlines()
            if not lines:
                continue
            if not lines[0].startswith("#"):
                section = lines[0].strip()
            body = " ".join(l for l in lines[1:] if not l.startswith("#"))
            words = body.split()
            for start in range(0, max(1, len(words)), max_words - overlap):
                piece = " ".join(words[start:start + max_words])
                if piece:
                    chunks.append(Chunk(path.name, section, piece))
    return chunks


class TfidfIndex:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.docs = [Counter(tokens(c.section + " " + c.text)) for c in chunks]
        df = Counter(t for d in self.docs for t in d)
        n = len(chunks)
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}
        self.vecs = [self._vec(d) for d in self.docs]

    def _vec(self, counts: Counter) -> dict[str, float]:
        v = {t: c * self.idf.get(t, 0.0) for t, c in counts.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}

    def search(self, query: str, k: int = 3) -> list[tuple[float, Chunk]]:
        q = self._vec(Counter(tokens(query)))
        scored = [(sum(w * vec.get(t, 0.0) for t, w in q.items()), c) for vec, c in zip(self.vecs, self.chunks)]
        return sorted((s for s in scored if s[0] > 0), key=lambda s: -s[0])[:k]


def build_prompt(question: str, hits: list[tuple[float, Chunk]]) -> str:
    context = "\n".join(f"[{i + 1}] ({c.source} > {c.section}) {c.text}" for i, (_, c) in enumerate(hits))
    return ("Answer using ONLY the numbered context. Cite sources like [1]. "
            "If the context does not contain the answer, say you don't know.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:")


def answer(question: str, index: TfidfIndex, llm: Callable[[str], str], min_score: float = 0.15) -> dict:
    hits = index.search(question)
    if not hits or hits[0][0] < min_score:
        return {"answer": "I don't know: nothing in the documents covers that.", "sources": []}
    return {"answer": llm(build_prompt(question, hits)),
            "sources": [f"{c.source} > {c.section}" for _, c in hits]}


def extractive_llm(prompt: str) -> str:
    """Offline stand-in for a model: returns the context sentence that best overlaps the question."""
    question = prompt.rsplit("Question:", 1)[1].split("\n")[0]
    q = set(tokens(question))
    best, best_i = "", 0
    for i, line in enumerate(prompt.split("Context:\n", 1)[1].split("\n\nQuestion:")[0].splitlines()):
        for sent in re.split(r"(?<=\.)\s", line.split(") ", 1)[-1]):
            score = len(q & set(tokens(sent)))
            if score > len(set(tokens(best)) & q):
                best, best_i = sent, i + 1
    return f"{best} [{best_i}]"
