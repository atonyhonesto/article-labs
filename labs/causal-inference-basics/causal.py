"""Correlation isn't causation, shown with numbers.

Question: does a new aero package make a car faster? Teams with bigger budgets
were more likely to adopt it AND were already faster, so the raw comparison
overstates the effect. Two standard fixes recover the truth:

* regression adjustment: model lap time from treatment plus the confounder
* inverse propensity weighting (IPW): reweight cars so adopters and non-adopters
  look alike on the confounder
"""
from __future__ import annotations

import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression

TRUE_EFFECT = -0.20      # the package really saves 0.2 s a lap


def simulate(n: int = 5000, seed: int = 0):
    rng = np.random.default_rng(seed)
    budget = rng.normal(0, 1, n)                                 # confounder
    p_adopt = 1 / (1 + np.exp(-1.5 * budget))
    adopted = (rng.random(n) < p_adopt).astype(int)
    lap = 80 - 0.6 * budget + TRUE_EFFECT * adopted + rng.normal(0, 0.3, n)
    return budget, adopted, lap


def naive(adopted, lap) -> float:
    return float(lap[adopted == 1].mean() - lap[adopted == 0].mean())


def regression_adjusted(budget, adopted, lap) -> float:
    X = np.column_stack([adopted, budget])
    return float(LinearRegression().fit(X, lap).coef_[0])


def ipw(budget, adopted, lap) -> float:
    ps = LogisticRegression().fit(budget.reshape(-1, 1), adopted).predict_proba(budget.reshape(-1, 1))[:, 1]
    ps = np.clip(ps, 0.01, 0.99)                                 # avoid exploding weights
    w1, w0 = adopted / ps, (1 - adopted) / (1 - ps)
    return float((w1 * lap).sum() / w1.sum() - (w0 * lap).sum() / w0.sum())
