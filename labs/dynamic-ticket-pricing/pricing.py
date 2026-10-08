"""Dynamic ticket pricing: learn demand, then price inside guardrails.

Demand per section is modelled as log-linear in price (constant elasticity),
fitted from past sales. Revenue = price x min(demand, seats left). The optimiser
searches prices between a floor and a ceiling, and caps any single change so
fans don't see wild swings.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Section:
    name: str
    seats_left: int
    floor: float
    ceiling: float
    current: float


def fit_elasticity(prices: np.ndarray, sold: np.ndarray) -> tuple[float, float]:
    """Fit log(sold) = a + b*log(price). Returns (a, b); b is the price elasticity (negative)."""
    b, a = np.polyfit(np.log(prices), np.log(np.maximum(sold, 1)), 1)
    return a, b


def demand(a: float, b: float, price: float) -> float:
    return float(np.exp(a + b * np.log(price)))


def best_price(section: Section, a: float, b: float, max_change: float = 0.15, step: float = 1.0) -> tuple[float, float]:
    lo = max(section.floor, section.current * (1 - max_change))
    hi = min(section.ceiling, section.current * (1 + max_change))
    grid = np.arange(lo, hi + 1e-9, step)
    revenue = [p * min(demand(a, b, p), section.seats_left) for p in grid]
    i = int(np.argmax(revenue))
    return float(grid[i]), float(revenue[i])


def intercept_for(demand_at_ref: float, ref_price: float, b: float) -> float:
    """Convert 'we sell N seats at $P' into the model's intercept."""
    return float(np.log(demand_at_ref) - b * np.log(ref_price))


def history(true_a: float, true_b: float, n: int = 40, seed: int = 3, lo: float = 40, hi: float = 160):
    rng = np.random.default_rng(seed)
    prices = rng.uniform(lo, hi, n)
    sold = np.exp(true_a + true_b * np.log(prices) + rng.normal(0, 0.15, n))
    return prices, sold
