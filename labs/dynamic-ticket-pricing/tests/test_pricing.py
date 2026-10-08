import unittest
from pricing import Section, best_price, fit_elasticity, history


class PricingTests(unittest.TestCase):
    def test_recovers_elasticity(self):
        a, b = fit_elasticity(*history(9.0, -1.8, n=200))
        self.assertAlmostEqual(b, -1.8, delta=0.15)

    def test_inelastic_demand_raises_price(self):
        sec = Section("x", 10_000, 10, 500, 100)
        price, _ = best_price(sec, 8.0, -0.6)
        self.assertGreater(price, 100)

    def test_guardrails_hold(self):
        sec = Section("x", 10_000, 95, 105, 100)
        for b in (-0.5, -3.0):
            price, _ = best_price(sec, 8.0, b)
            self.assertTrue(95 <= price <= 105)

    def test_sellout_caps_revenue(self):
        sec = Section("x", 50, 10, 500, 100)
        price, rev = best_price(sec, 12.0, -1.2)
        self.assertLessEqual(rev, price * 50 + 1e-6)


if __name__ == "__main__":
    unittest.main()
