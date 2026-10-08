<sub>[← all labs](../../README.md)</sub>

# Retrieval-augmented generation, without the framework

> LangChain packages a simple loop: chunk, index, retrieve, prompt, answer with citations. Here's the loop.

`Python` · `stdlib`

**Companion to:**
- [LangChain](https://www.linkedin.com/pulse/langchain-tony-honesto-gl8oc/)

## What it shows

- Chunking documents by section with overlap, keeping the source on every chunk.
- A TF-IDF index and cosine-similarity retrieval.
- A prompt that tells the model to answer only from numbered context and cite it.
- Refusing to answer when retrieval finds nothing relevant, rather than letting the model guess.
- A pluggable `llm` callable; an offline extractive stand-in keeps the lab key-free.

## Run it

```bash
bash labs/rag-retrieval-pipeline/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Indexed 7 chunks

Q: What is the pit lane speed limit in the race?
A: The pit lane speed limit is 60 km/h during practice and 80 km/h during the race. [1]
   sources: ['sporting-regulations.md > Pit lane', 'sporting-regulations.md > Safety car']

Q: How many sets of dry tires does a driver get?
A: Each driver receives 13 sets of dry tires per weekend. [1]
   sources: ['technical-regulations.md > Tires', 'technical-regulations.md > Weight']

Q: Who won the 1987 championship?
A: I don't know: nothing in the documents covers that.
   sources: []
```

## What's in here

| File | Purpose |
|---|---|
| `rag.py` | Chunker, index, prompt builder, answer function and offline model |
| `docs/` | Two fictional regulation documents |
| `demo.py` | Three questions, including one the documents can't answer |
| `tests/` | Retrieval, prompt, citation and refusal tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| TF-IDF | An embedding model and a vector store (pgvector, OpenSearch, Pinecone) |
| Extractive stand-in | Any chat model through the same `llm(prompt)` interface |
| Fixed threshold | Re-ranking and evaluation against a labelled question set |
