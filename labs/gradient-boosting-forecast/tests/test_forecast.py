import unittest
from forecast import backtest, daily_sales, features


class ForecastTests(unittest.TestCase):
    def test_features_use_only_the_past(self):
        f = features(daily_sales(200))
        self.assertTrue((f.lag_7.iloc[10:] == f.sales.shift(7).iloc[10:]).all())

    def test_model_beats_naive_baseline(self):
        res = backtest(daily_sales(), folds=4)
        self.assertLess(res.mape_model.mean(), res.mape_naive.mean())


if __name__ == "__main__":
    unittest.main()
