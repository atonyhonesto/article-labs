"""Reinforcement learning from scratch: when should we pit?

State: (laps remaining bucket, tire wear bucket). Actions: stay out or pit.
Reward: minus the time the lap costs (worn tires are slower, a stop costs a
fixed loss). Tabular Q-learning learns the policy from simulated stints, with no
model of the race given to the agent. The same loop is what a PyTorch DQN
replaces the table with when the state gets too big to enumerate.
"""
from __future__ import annotations

import numpy as np

STAY, PIT = 0, 1
LAPS = 40
WEAR_BUCKETS = 10
LAP_BUCKETS = 10
PIT_LOSS = 20.0


def lap_cost(wear: int) -> float:
    """Seconds lost to tire wear this lap (wear 0-9), growing faster as tires age."""
    return 0.25 * wear + 0.08 * wear ** 2


def bucket(laps_left: int) -> int:
    return min(LAP_BUCKETS - 1, laps_left * LAP_BUCKETS // (LAPS + 1))


def step(laps_left: int, wear: int, action: int) -> tuple[int, int, float]:
    cost = 0.0
    if action == PIT:
        cost += PIT_LOSS
        wear = 0
    cost += lap_cost(wear)
    return laps_left - 1, min(WEAR_BUCKETS - 1, wear + 1), -cost


def train(episodes: int = 30000, alpha: float = 0.1, gamma: float = 1.0, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    q = np.zeros((LAP_BUCKETS, WEAR_BUCKETS, 2))
    for ep in range(episodes):
        eps = max(0.02, 1.0 - ep / (0.6 * episodes))          # explore early, exploit later
        laps_left, wear = LAPS, int(rng.integers(0, WEAR_BUCKETS))
        while laps_left > 0:
            s = (bucket(laps_left), wear)
            a = int(rng.integers(2)) if rng.random() < eps else int(np.argmax(q[s]))
            nl, nw, r = step(laps_left, wear, a)
            target = r if nl == 0 else r + gamma * q[bucket(nl), nw].max()
            q[s + (a,)] += alpha * (target - q[s + (a,)])
            laps_left, wear = nl, nw
    return q


def run_policy(q: np.ndarray, start_wear: int = 0) -> tuple[float, list[int]]:
    laps_left, wear, total, stops = LAPS, start_wear, 0.0, []
    while laps_left > 0:
        a = int(np.argmax(q[bucket(laps_left), wear]))
        if a == PIT:
            stops.append(LAPS - laps_left + 1)
        laps_left, wear, r = step(laps_left, wear, a)
        total -= r
    return total, stops


def never_pit(start_wear: int = 0) -> float:
    laps_left, wear, total = LAPS, start_wear, 0.0
    while laps_left > 0:
        laps_left, wear, r = step(laps_left, wear, STAY)
        total -= r
    return total


def optimal_cost(start_wear: int = 0) -> float:
    """Exact optimum by dynamic programming over (laps left, wear), for checking the learner."""
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def best(laps_left: int, wear: int) -> float:
        if laps_left == 0:
            return 0.0
        options = []
        for a in (STAY, PIT):
            nl, nw, r = step(laps_left, wear, a)
            options.append(-r + best(nl, nw))
        return min(options)

    return best(LAPS, start_wear)
