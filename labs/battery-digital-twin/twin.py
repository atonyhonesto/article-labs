"""A battery digital twin: a physics model run alongside the real cell.

Model: first-order equivalent circuit (open-circuit voltage + series resistance
+ one RC pair) with Coulomb counting for state of charge and a lumped thermal
model. The twin receives the same current the real cell sees and predicts its
voltage; a growing gap between predicted and measured voltage is the early sign
of ageing (resistance rise) before capacity visibly fades.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def ocv(soc: float) -> float:
    """Open-circuit voltage of an NMC-like cell, volts."""
    soc = min(max(soc, 0.0), 1.0)
    return 3.0 + 1.2 * soc - 0.25 * np.exp(-12 * soc) + 0.05 * np.sin(3 * soc)


@dataclass
class CellParams:
    capacity_ah: float = 5.0
    r0_ohm: float = 0.015
    r1_ohm: float = 0.010
    c1_f: float = 2000.0
    thermal_mass_j_per_k: float = 90.0
    cooling_w_per_k: float = 0.6


@dataclass
class Twin:
    p: CellParams
    soc: float = 0.9
    v_rc: float = 0.0
    temp_c: float = 25.0
    ambient_c: float = 25.0
    history: list = field(default_factory=list)

    def step(self, current_a: float, dt: float) -> float:
        """Advance by dt seconds with discharge current (A, positive = discharge). Returns terminal voltage."""
        self.soc -= current_a * dt / (self.p.capacity_ah * 3600)
        tau = self.p.r1_ohm * self.p.c1_f
        self.v_rc = self.v_rc * np.exp(-dt / tau) + self.p.r1_ohm * (1 - np.exp(-dt / tau)) * current_a
        heat = current_a ** 2 * (self.p.r0_ohm + self.p.r1_ohm)
        self.temp_c += (heat - self.p.cooling_w_per_k * (self.temp_c - self.ambient_c)) * dt / self.p.thermal_mass_j_per_k
        v = ocv(self.soc) - current_a * self.p.r0_ohm - self.v_rc
        self.history.append((self.soc, v, self.temp_c))
        return float(v)


def drive_cycle(seconds: int = 1800, seed: int = 0) -> np.ndarray:
    """Bursty load: cruise, hard pulls and regen, one sample per second."""
    rng = np.random.default_rng(seed)
    base = 4 + 3 * np.sin(np.arange(seconds) / 40)
    pulls = (rng.random(seconds) < 0.05) * rng.uniform(10, 20, seconds)
    regen = -((rng.random(seconds) < 0.03) * rng.uniform(3, 8, seconds))
    return base + pulls + regen


def monitor(measured_v: np.ndarray, predicted_v: np.ndarray, window: int = 120, limit_v: float = 0.02) -> int | None:
    """First second at which the rolling mean |error| exceeds the limit (the twin says: inspect this cell)."""
    err = np.abs(measured_v - predicted_v)
    roll = np.convolve(err, np.ones(window) / window, mode="valid")
    hits = np.flatnonzero(roll > limit_v)
    return int(hits[0] + window) if hits.size else None
