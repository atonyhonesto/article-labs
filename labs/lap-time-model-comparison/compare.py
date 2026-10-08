"""Compare model families on lap-time prediction, the honest way.

Laps from the same stint are correlated, so a random split leaks information.
GroupKFold keeps whole stints out of training, which is how the model will meet
a new stint on race day.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["tire_age", "fuel_kg", "track_temp", "compound_soft", "traffic"]


def make_data(seed: int = 11, stints: int = 60, laps: int = 25) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for s in range(stints):
        soft = int(rng.random() < 0.5)
        driver_offset = rng.normal(0, 0.25)            # unobserved: shared within a stint
        temp = rng.uniform(22, 48)
        for age in range(laps):
            traffic = int(rng.random() < 0.15)
            fuel = 100 - 3.2 * age
            cliff = 1.8 if soft and age > 16 else 0.0  # non-linear: softs fall off a cliff
            t = (90 - 0.6 * soft + 0.04 * age + cliff + 0.0028 * fuel
                 + 0.01 * (temp - 35) * age / 10 + 0.7 * traffic + driver_offset + rng.normal(0, 0.1))
            rows.append({"stint": s, "tire_age": age, "fuel_kg": fuel, "track_temp": temp,
                         "compound_soft": soft, "traffic": traffic, "lap_time": t})
    return pd.DataFrame(rows)


MODELS = {
    "ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
    "random_forest": RandomForestRegressor(n_estimators=200, min_samples_leaf=3, random_state=0),
    "gradient_boosting": GradientBoostingRegressor(random_state=0),
}


def evaluate(df: pd.DataFrame) -> pd.DataFrame:
    X, y, groups = df[FEATURES], df["lap_time"], df["stint"]
    out = []
    for name, model in MODELS.items():
        grouped = -cross_val_score(model, X, y, groups=groups, cv=GroupKFold(5),
                                   scoring="neg_mean_absolute_error")
        leaky = -cross_val_score(model, X, y, cv=KFold(5, shuffle=True, random_state=0),
                                 scoring="neg_mean_absolute_error")
        out.append({"model": name, "mae_grouped_s": grouped.mean(), "mae_random_split_s": leaky.mean()})
    return pd.DataFrame(out).sort_values("mae_grouped_s").reset_index(drop=True)
