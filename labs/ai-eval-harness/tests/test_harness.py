import unittest
from harness import Criteria, Result, candidate_model, decide, evaluate, keyword_baseline


class HarnessTests(unittest.TestCase):
    def test_baseline_misses_outages(self):
        self.assertGreater(evaluate("b", keyword_baseline).missed_outages, 0)

    def test_candidate_goes(self):
        ok, why = decide(evaluate("c", candidate_model, 0.001), evaluate("b", keyword_baseline), Criteria())
        self.assertTrue(ok, why)

    def test_one_missed_outage_blocks_launch(self):
        cand = Result("c", 0.99, 1, 0.0, 10)
        ok, why = decide(cand, Result("b", 0.5, 3, 0, 1), Criteria())
        self.assertFalse(ok)
        self.assertIn("missed 1 outage(s)", why)


if __name__ == "__main__":
    unittest.main()
