"""Gradient-boosted demand forecasting, evaluated like a forecast (not like a classifier).

* Lag and calendar features built only from the past (no peeking at the target).
* Rolling-origin backtest: train on everything before a cutoff, forecast the next
  week, move the cutoff, repeat.
* Always compare with a naive seasonal baseline ("same day last week"): a model
  that can't beat it isn't worth shipping.

Uses scikit-learn's HistGradientBoostingRegressor. To use XGBoost, swap the model
for `xgboost.XGBRegressor(n_estimators=400, max_depth=4, learning_rate=0.05)`;
nothing else changes.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor


def daily_sales(days: int = 730, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    d = pd.date_range("2024-01-01", periods=days, freq="D")
    trend = np.linspace(100, 140, days)
    weekly = 1 + 0.25 * np.isin(d.dayofweek, [4, 5])               # Fri/Sat busier
    yearly = 1 + 0.15 * np.sin(2 * np.pi * d.dayofyear / 365.25)
    promo = rng.random(days) < 0.06
    y = trend * weekly * yearly * np.where(promo, 1.35, 1.0) + rng.normal(0, 6, days)
    return pd.DataFrame({"date": d, "sales": y, "promo": promo.astype(int)})


def features(df: pd.DataFrame) -> pd.DataFrame:
    f = df.copy()
    f["dow"] = f.date.dt.dayofweek
    f["doy_sin"] = np.sin(2 * np.pi * f.date.dt.dayofyear / 365.25)
    f["doy_cos"] = np.cos(2 * np.pi * f.date.dt.dayofyear / 365.25)
    for lag in (7, 14, 28):
        f[f"lag_{lag}"] = f.sales.shift(lag)
    f["roll_mean_28"] = f.sales.shift(7).rolling(28).mean()        # shifted: only past information
    return f.dropna().reset_index(drop=True)


FEATS = ["dow", "doy_sin", "doy_cos", "promo", "lag_7", "lag_14", "lag_28", "roll_mean_28"]


def backtest(df: pd.DataFrame, folds: int = 8, horizon: int = 7) -> pd.DataFrame:
    f = features(df)
    rows = []
    for k in range(folds, 0, -1):
        cut = len(f) - k * horizon
        train, test = f.iloc[:cut], f.iloc[cut:cut + horizon]
        model = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=0)
        model.fit(train[FEATS], train.sales)
        pred = model.predict(test[FEATS])
        naive = test.lag_7.to_numpy()
        rows.append({"cutoff": test.date.iloc[0].date(),
                     "mape_model": float(np.mean(np.abs(pred - test.sales) / test.sales)),
                     "mape_naive": float(np.mean(np.abs(naive - test.sales) / test.sales))})
    return pd.DataFrame(rows)
