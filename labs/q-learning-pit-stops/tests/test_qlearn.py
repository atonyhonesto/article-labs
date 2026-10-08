import unittest
from qlearn import never_pit, optimal_cost, run_policy, train


class QLearnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = train(episodes=15000)

    def test_learned_policy_beats_never_pitting(self):
        self.assertLess(run_policy(self.q, 0)[0], never_pit(0))

    def test_close_to_the_true_optimum(self):
        self.assertLess(run_policy(self.q, 0)[0], optimal_cost(0) * 1.05)

    def test_does_not_pit_on_the_last_lap(self):
        _, stops = run_policy(self.q, 0)
        self.assertNotIn(40, stops)

    def test_worn_start_pits_early(self):
        _, stops = run_policy(self.q, 9)
        self.assertTrue(stops and stops[0] <= 5)


if __name__ == "__main__":
    unittest.main()
