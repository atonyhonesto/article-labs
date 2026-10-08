import unittest
from pathlib import Path

from rag import TfidfIndex, answer, build_prompt, extractive_llm, load_chunks

DOCS = Path(__file__).resolve().parent.parent / "docs"


class RagTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = TfidfIndex(load_chunks(DOCS))

    def test_retrieves_the_right_section(self):
        top = self.index.search("tire blankets temperature")[0][1]
        self.assertEqual(top.section, "Tires")

    def test_prompt_restricts_model_to_context(self):
        p = build_prompt("q?", self.index.search("fuel flow"))
        self.assertIn("ONLY the numbered context", p)
        self.assertIn("[1]", p)

    def test_answers_with_citation(self):
        r = answer("What is the minimum weight of the car?", self.index, extractive_llm)
        self.assertIn("798", r["answer"])
        self.assertTrue(r["sources"])

    def test_refuses_when_nothing_relevant(self):
        r = answer("best pizza in Indianapolis", self.index, extractive_llm)
        self.assertEqual(r["sources"], [])


if __name__ == "__main__":
    unittest.main()
