"""From raw RFID location pings to the stats a broadcast shows.

Tags report (t, x, y) in metres at ~10 Hz. Real feeds jitter and drop packets,
so positions are smoothed and time gaps are respected before anything is derived.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

SPRINT_MPS = 7.0          # ~15.7 mph, a common "high-speed running" threshold
SPRINT_EXIT_MPS = 6.0     # hysteresis: a sprint ends only once speed drops well below the entry


def count_sprints(speed: np.ndarray) -> int:
    """Count sprints with hysteresis so noise around the threshold isn't double-counted."""
    count, sprinting = 0, False
    for v in speed:
        if not sprinting and v >= SPRINT_MPS:
            sprinting, count = True, count + 1
        elif sprinting and v < SPRINT_EXIT_MPS:
            sprinting = False
    return count


@dataclass
class PlayerStats:
    distance_m: float
    top_speed_mps: float
    sprints: int
    max_accel_mps2: float


def smooth(values: np.ndarray, window: int = 5) -> np.ndarray:
    """Centred moving average; edges use the available samples."""
    window = max(1, window | 1)                 # odd, so the output keeps its length
    kernel = np.ones(window) / window
    padded = np.pad(values, (window // 2, window // 2), mode="edge")
    return np.convolve(padded, kernel, mode="valid")


def smooth_segments(t: np.ndarray, values: np.ndarray, max_gap_s: float, window: int = 5) -> np.ndarray:
    """Smooth each unbroken run of pings separately so a dropout never blends two positions."""
    out = np.empty_like(values, dtype=float)
    breaks = np.flatnonzero(np.diff(t) > max_gap_s) + 1
    for seg in np.split(np.arange(values.size), breaks):
        out[seg] = smooth(values[seg], min(window, seg.size))
    return out


def analyse(t: np.ndarray, x: np.ndarray, y: np.ndarray, max_gap_s: float = 0.5) -> PlayerStats:
    xs, ys = smooth_segments(t, x, max_gap_s), smooth_segments(t, y, max_gap_s)
    dt = np.diff(t)
    step = np.hypot(np.diff(xs), np.diff(ys))
    ok = dt <= max_gap_s                      # never integrate across a dropout
    speed = np.where(ok, step / np.where(dt > 0, dt, np.inf), 0.0)
    speed = smooth(speed, 5)
    accel = np.diff(speed) / np.where(dt[1:] > 0, dt[1:], np.inf)
    accel = np.where(ok[1:] & ok[:-1], accel, 0.0)
    sprints = count_sprints(speed)
    return PlayerStats(float(step[ok].sum()), float(speed.max(initial=0)), sprints,
                       float(np.abs(accel).max(initial=0)))


def simulate_route(seed: int = 1, hz: int = 10, seconds: int = 60):
    """Jog, two sprints, a dropout, plus tag jitter."""
    rng = np.random.default_rng(seed)
    t = np.arange(0, seconds, 1 / hz)
    v = np.full_like(t, 3.0)
    v[(t > 10) & (t < 14)] = 8.5
    v[(t > 35) & (t < 38)] = 9.2
    v = smooth(v, 2 * hz + 1)                 # players ramp up over ~2 s, not instantly
    x = np.cumsum(v / hz) + rng.normal(0, 0.05, t.size)
    y = 20 + rng.normal(0, 0.05, t.size)
    keep = ~((t > 50) & (t < 52))             # 2 s packet loss
    return t[keep], x[keep], y[keep]
