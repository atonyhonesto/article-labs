from pathlib import Path

from rag import TfidfIndex, answer, extractive_llm, load_chunks

index = TfidfIndex(load_chunks(Path(__file__).with_name("docs")))
print(f"Indexed {len(index.chunks)} chunks")
for q in ("What is the pit lane speed limit in the race?",
          "How many sets of dry tires does a driver get?",
          "Who won the 1987 championship?"):
    r = answer(q, index, extractive_llm)
    print(f"\nQ: {q}\nA: {r['answer']}\n   sources: {r['sources'][:2]}")
