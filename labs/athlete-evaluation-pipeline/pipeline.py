"""An athlete-evaluation pipeline where every preprocessing step lives inside the model.

Imputation, scaling and encoding are fitted inside each CV fold, so nothing from
the validation athletes leaks into training. The same object then scores new
prospects with no hand-copied preprocessing.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ["sprint_40yd_s", "vertical_in", "bench_reps", "games_played", "efficiency"]
CATEGORICAL = ["position", "conference_tier"]


def prospects(n: int = 1200, seed: int = 2) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "sprint_40yd_s": rng.normal(4.6, 0.15, n),
        "vertical_in": rng.normal(33, 3, n),
        "bench_reps": rng.normal(20, 5, n),
        "games_played": rng.integers(10, 50, n),
        "efficiency": rng.normal(0, 1, n),
        "position": rng.choice(["WR", "RB", "LB", "CB"], n),
        "conference_tier": rng.choice(["P4", "G5", "FCS"], n, p=[0.5, 0.35, 0.15]),
    })
    score = (-(df.sprint_40yd_s - 4.6) * 8 + (df.vertical_in - 33) * 0.15 + df.efficiency * 1.2
             + df.conference_tier.map({"P4": 0.5, "G5": 0.0, "FCS": -0.5}) + rng.normal(0, 1, n))
    df["made_roster"] = (score > np.quantile(score, 0.7)).astype(int)
    for col in ("vertical_in", "bench_reps"):          # combine data is often missing
        df.loc[rng.random(n) < 0.2, col] = np.nan
    return df


def build() -> Pipeline:
    pre = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return Pipeline([("prep", pre), ("model", LogisticRegression(C=0.5, max_iter=1000))])


def cross_validated_auc(df: pd.DataFrame) -> float:
    X, y = df[NUMERIC + CATEGORICAL], df["made_roster"]
    proba = cross_val_predict(build(), X, y, cv=StratifiedKFold(5, shuffle=True, random_state=0),
                              method="predict_proba")[:, 1]
    return float(roc_auc_score(y, proba))
