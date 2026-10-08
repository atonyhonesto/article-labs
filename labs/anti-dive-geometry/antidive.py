"""Front anti-dive from suspension geometry (side view, 2D).

Braking load transfer pushes the nose down. If the wishbones are inclined, part
of the braking force is reacted through the links instead of the springs. For
outboard (hub-mounted) brakes the side-view instant centre (IC) of the front
suspension sets it:

    anti-dive % = tan(theta) * wheelbase / CG height * front brake share * 100

where theta is the angle of the line from the tire contact patch to the IC.
Coordinates: x forward from the front contact patch, z up from the ground, metres.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Wishbone:
    """Side-view projection of a wishbone: chassis pickup and upright ball joint."""
    chassis: tuple[float, float]
    upright: tuple[float, float]


def intersect(a1, a2, b1, b2) -> np.ndarray | None:
    """Intersection of line a1-a2 with line b1-b2, or None if parallel."""
    a1, a2, b1, b2 = map(np.asarray, (a1, a2, b1, b2))
    da, db = a2 - a1, b2 - b1
    denom = da[0] * db[1] - da[1] * db[0]
    if abs(denom) < 1e-12:
        return None
    t = ((b1[0] - a1[0]) * db[1] - (b1[1] - a1[1]) * db[0]) / denom
    return a1 + t * da


def anti_dive_percent(upper: Wishbone, lower: Wishbone, wheelbase: float, cg_height: float,
                      front_brake_share: float) -> float:
    ic = intersect(upper.chassis, upper.upright, lower.chassis, lower.upright)
    if ic is None:                                # parallel links: no anti-dive
        return 0.0
    if ic[0] == 0:
        return float("inf")
    # Line from the contact patch (0, 0) to an IC behind the axle (x < 0) and above
    # ground resists dive; an IC ahead of the axle adds dive (negative percentage).
    tan_theta = ic[1] / -ic[0]
    return float(tan_theta * wheelbase / cg_height * front_brake_share * 100)


def pitch_change_deg(decel_g: float, mass: float, cg_height: float, wheelbase: float,
                     front_rate_n_per_m: float, anti_pct: float) -> float:
    """Nose-down pitch from front spring compression after anti-dive removes its share of the load."""
    transfer = mass * 9.81 * decel_g * cg_height / wheelbase
    spring_load = transfer * (1 - anti_pct / 100)
    dz = spring_load / front_rate_n_per_m
    return float(np.degrees(np.arctan(dz / wheelbase)))
