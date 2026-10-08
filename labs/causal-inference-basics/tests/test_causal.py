import unittest
from causal import TRUE_EFFECT, ipw, naive, regression_adjusted, simulate


class CausalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b, cls.a, cls.y = simulate()

    def test_naive_is_badly_biased(self):
        self.assertLess(naive(self.a, self.y), TRUE_EFFECT - 0.3)

    def test_adjustments_recover_truth(self):
        self.assertAlmostEqual(regression_adjusted(self.b, self.a, self.y), TRUE_EFFECT, delta=0.03)
        self.assertAlmostEqual(ipw(self.b, self.a, self.y), TRUE_EFFECT, delta=0.06)


if __name__ == "__main__":
    unittest.main()
