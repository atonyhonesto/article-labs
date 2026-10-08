import unittest
from compare import evaluate, make_data


class CompareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = evaluate(make_data(stints=40))

    def test_tree_model_beats_linear_on_the_tire_cliff(self):
        best = self.res.iloc[0]["model"]
        self.assertIn(best, {"random_forest", "gradient_boosting"})

    def test_random_split_looks_optimistic(self):
        # shared stint effects leak across a random split, flattering every model
        self.assertTrue((self.res.mae_random_split_s <= self.res.mae_grouped_s + 1e-9).all())


if __name__ == "__main__":
    unittest.main()
