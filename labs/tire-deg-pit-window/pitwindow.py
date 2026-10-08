"""Learn tire fall-off from lap data, then pick the pit lap that minimises total race time."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


def simulate_stints(seed: int = 7, stints: int = 40, laps: int = 30) -> pd.DataFrame:
    """Synthetic practice data: lap time grows with tire age (quadratically) and drops as fuel burns."""
    rng = np.random.default_rng(seed)
    rows = []
    for s in range(stints):
        base = 92.0 + rng.normal(0, 0.3)
        temp = rng.uniform(25, 45)
        for age in range(laps):
            fuel_kg = 100 - 1.6 * (s % 3) * 10 - 1.6 * age
            t = (base + 0.035 * age + 0.0022 * age**2 * (temp / 35)
                 + 0.03 * max(fuel_kg, 0) / 10 + rng.normal(0, 0.12))
            rows.append({"stint": s, "tire_age": age, "track_temp": temp,
                         "fuel_kg": max(fuel_kg, 0), "lap_time": t})
    return pd.DataFrame(rows)


def fit_degradation(df: pd.DataFrame):
    """Polynomial model of lap time from tire age, track temp and fuel load."""
    model = make_pipeline(PolynomialFeatures(degree=2, include_bias=False), LinearRegression())
    model.fit(df[["tire_age", "track_temp", "fuel_kg"]], df["lap_time"])
    return model


def race_time(model, race_laps: int, pit_lap: int, track_temp: float,
              pit_loss_s: float = 21.0, fuel_per_lap: float = 1.6, start_fuel: float = 100) -> float:
    """Total time for a one-stop race pitting at the end of `pit_lap`."""
    laps = np.arange(race_laps)
    age = np.where(laps < pit_lap, laps, laps - pit_lap)
    fuel = np.maximum(start_fuel - fuel_per_lap * laps, 0)
    X = pd.DataFrame({"tire_age": age, "track_temp": track_temp, "fuel_kg": fuel})
    return float(model.predict(X).sum() + pit_loss_s)


def best_pit_lap(model, race_laps: int, track_temp: float, window: tuple[int, int]) -> tuple[int, float, dict]:
    times = {lap: race_time(model, race_laps, lap, track_temp) for lap in range(window[0], window[1] + 1)}
    lap = min(times, key=times.get)
    return lap, times[lap], times
