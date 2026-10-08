"""Monte Carlo pit strategy under caution risk (oval racing).

A green-flag stop costs a lap's worth of time; a stop under caution costs far
less because the field is slowed. Cautions are random, so a strategy is judged on
its distribution of outcomes, not one race.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Track:
    laps: int = 200
    fuel_window: int = 60          # max laps on a tank
    green_lap_s: float = 49.0
    green_stop_loss_s: float = 38.0
    caution_stop_loss_s: float = 12.0
    caution_rate: float = 0.03     # chance a caution starts on any green lap
    caution_laps: int = 5
    deg_s_per_lap: float = 0.035   # tire fall-off


def run_race(track: Track, plan: str, rng: np.random.Generator) -> float:
    """Return race time for one simulated race.

    plan = "fixed": stop every fuel_window - 2 laps regardless.
    plan = "opportunistic": also stop under any caution once 60% into a stint.
    """
    t, age, since_stop, caution_left = 0.0, 0, 0, 0
    for lap in range(track.laps):
        under_caution = caution_left > 0
        if not under_caution and rng.random() < track.caution_rate:
            caution_left, under_caution = track.caution_laps, True
        must_stop = since_stop >= track.fuel_window - 2 and lap < track.laps - 2
        want_stop = (plan == "opportunistic" and under_caution
                     and since_stop >= 0.6 * track.fuel_window and lap < track.laps - 10)
        if must_stop or want_stop:
            t += track.caution_stop_loss_s if under_caution else track.green_stop_loss_s
            age = since_stop = 0
        lap_s = track.green_lap_s + track.deg_s_per_lap * age
        t += lap_s * (1.6 if under_caution else 1.0)
        age += 1
        since_stop += 1
        caution_left = max(0, caution_left - 1)
    return t


def compare(track: Track, n: int = 4000, seed: int = 0) -> dict[str, dict[str, float]]:
    out = {}
    for plan in ("fixed", "opportunistic"):
        rng = np.random.default_rng(seed)          # same cautions for both plans: a fair comparison
        times = np.array([run_race(track, plan, rng) for _ in range(n)])
        out[plan] = {"mean_s": float(times.mean()), "p10_s": float(np.percentile(times, 10)),
                     "p90_s": float(np.percentile(times, 90))}
    return out
