"""Hybrid energy budget over a lap: what losing the MGU-H changes.

Simplified 2026-style model: the MGU-K harvests under braking and deploys on
straights; the battery has a usable window. Pre-2026 cars also recovered energy
from exhaust heat via the MGU-H, which could top up the battery on the straights.
Without it, every joule must come from braking, so deployment has to be rationed.

Numbers are illustrative, not regulation values.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Segment:
    name: str
    kind: str          # "brake" or "straight" or "corner"
    seconds: float


LAP = [Segment("T1 brake", "brake", 2.0), Segment("T1-T3", "corner", 9.0),
       Segment("Back straight", "straight", 12.0), Segment("T4 brake", "brake", 2.5),
       Segment("Infield", "corner", 18.0), Segment("Main straight", "straight", 14.0),
       Segment("T10 brake", "brake", 1.5), Segment("Final sector", "corner", 20.0)]


@dataclass(frozen=True)
class PowerUnit:
    mguk_kw: float
    mguh_kw: float              # 0 for 2026-style units
    battery_mj: float = 4.0


def simulate_lap(pu: PowerUnit, soc_start_mj: float, deploy_fraction: float = 1.0) -> tuple[float, float]:
    """Return (deployed MJ, end-of-lap state of charge MJ). Deployment stops if the battery empties."""
    soc, deployed = soc_start_mj, 0.0
    for seg in LAP:
        if seg.kind == "brake":
            soc = min(pu.battery_mj, soc + pu.mguk_kw * seg.seconds / 1000)
        elif seg.kind == "straight":
            # MGU-H recovery and MGU-K deployment happen together on the straight
            available = soc + pu.mguh_kw * seg.seconds / 1000
            want = pu.mguk_kw * seg.seconds / 1000 * deploy_fraction
            use = min(want, available)
            soc = min(pu.battery_mj, available - use)
            deployed += use
    return deployed, soc


def sustainable_deploy_fraction(pu: PowerUnit, laps: int = 10) -> float:
    """Highest flat deploy fraction whose state of charge doesn't decline lap over lap."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        soc = pu.battery_mj
        for _ in range(laps):
            _, soc = simulate_lap(pu, soc, mid)
        if soc >= pu.battery_mj - 1e-6:
            lo = mid
        else:
            hi = mid
    return lo
