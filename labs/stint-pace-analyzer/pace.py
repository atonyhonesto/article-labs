"""Stint pace analysis in the spirit of FastF1 notebooks, on synthetic laps.

Raw lap times mislead: in-laps and out-laps are slow, and cars get faster as fuel
burns. This splits laps into stints, drops the pit laps and safety-car laps,
corrects for fuel, then compares drivers on like-for-like pace.

Swap `synthetic_session()` for FastF1 (`session.laps`) and the rest works unchanged:
it uses the same column names (Driver, LapNumber, LapTime_s, Stint, PitInTime, PitOutTime).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FUEL_EFFECT_S_PER_LAP = 0.055   # each lap of fuel burned makes the car ~0.055 s quicker


def synthetic_session(seed: int = 5, laps: int = 55) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    drivers = {"AAA": 0.0, "BBB": 0.18, "CCC": 0.42}
    pits = {"AAA": [18, 38], "BBB": [24], "CCC": [15, 33]}
    sc_laps = set(range(28, 31))
    rows = []
    for drv, offset in drivers.items():
        stint, age = 1, 0
        for lap in range(1, laps + 1):
            t = 93.0 + offset + 0.06 * age - FUEL_EFFECT_S_PER_LAP * lap + rng.normal(0, 0.15)
            pit_in = lap in pits[drv]
            pit_out = (lap - 1) in pits[drv]
            if pit_in: t += 18
            if pit_out: t += 4
            if lap in sc_laps: t += 25
            rows.append({"Driver": drv, "LapNumber": lap, "LapTime_s": t, "Stint": stint,
                         "PitInTime": pit_in, "PitOutTime": pit_out, "TrackStatus": "4" if lap in sc_laps else "1"})
            age += 1
            if pit_in:
                stint, age = stint + 1, 0
    return pd.DataFrame(rows)


def representative_laps(laps: pd.DataFrame) -> pd.DataFrame:
    """Green-flag laps that are neither in-laps nor out-laps, fuel-corrected to an empty car."""
    clean = laps[(~laps.PitInTime) & (~laps.PitOutTime) & (laps.TrackStatus == "1")].copy()
    max_lap = laps.LapNumber.max()
    clean["Corrected_s"] = clean.LapTime_s + FUEL_EFFECT_S_PER_LAP * (clean.LapNumber - max_lap)
    return clean


def driver_pace(laps: pd.DataFrame) -> pd.DataFrame:
    """Median pace after removing fuel effect AND tire age.

    Without the tire-age correction a driver on more, shorter stints looks faster
    simply because they ran fresher rubber more often.
    """
    rep = representative_laps(laps)
    rep["age"] = rep.groupby(["Driver", "Stint"]).cumcount()
    deg = stint_degradation(laps).deg_s_per_lap.median()
    rep["Pace_s"] = rep.Corrected_s - deg * rep.age
    g = rep.groupby("Driver").Pace_s
    out = pd.DataFrame({"median_s": g.median(), "std_s": g.std(), "laps_used": g.size()})
    out["gap_s"] = out.median_s - out.median_s.min()
    return out.sort_values("median_s")


def stint_degradation(laps: pd.DataFrame) -> pd.DataFrame:
    """Slope of corrected lap time vs lap-in-stint: seconds lost per lap of tire age."""
    rep = representative_laps(laps)
    rep["age"] = rep.groupby(["Driver", "Stint"]).cumcount()
    rows = []
    for (drv, stint), g in rep.groupby(["Driver", "Stint"]):
        if len(g) >= 5:
            rows.append({"Driver": drv, "Stint": stint, "deg_s_per_lap": np.polyfit(g.age, g.Corrected_s, 1)[0]})
    return pd.DataFrame(rows)
