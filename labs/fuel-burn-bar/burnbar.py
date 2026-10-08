"""A broadcast-style "burn bar": is this car using fuel faster than it can afford?

Each lap the car reports fuel used. The target is the fuel left divided by laps
left. The bar shows the gap; a rolling average stops one slow lap under caution
from making the graphic jump around.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass
class BurnReading:
    lap: int
    used_this_lap: float
    rolling_avg: float
    target_per_lap: float
    fuel_left: float

    @property
    def delta_pct(self) -> float:
        """Positive = burning more than the target allows (in trouble)."""
        return (self.rolling_avg / self.target_per_lap - 1) * 100 if self.target_per_lap > 0 else 0.0

    @property
    def status(self) -> str:
        d = self.delta_pct
        return "ON TARGET" if abs(d) <= 1.5 else ("SAVE FUEL" if d > 0 else "CAN PUSH")

    def bar(self, width: int = 21) -> str:
        """ASCII gauge: centre is on-target, right is over-burning."""
        pos = max(0, min(width - 1, width // 2 + round(self.delta_pct / 2)))
        return "".join("|" if i == width // 2 else ("#" if i == pos else "-") for i in range(width))


class BurnBar:
    def __init__(self, fuel_start: float, race_laps: int, window: int = 3):
        self.fuel_left = fuel_start
        self.race_laps = race_laps
        self.recent: deque[float] = deque(maxlen=window)

    def update(self, lap: int, used: float, under_caution: bool = False) -> BurnReading:
        self.fuel_left -= used
        if not under_caution:            # caution laps would flatter the average
            self.recent.append(used)
        laps_left = self.race_laps - lap
        target = self.fuel_left / laps_left if laps_left else 0.0
        avg = sum(self.recent) / len(self.recent) if self.recent else used
        return BurnReading(lap, used, avg, target, self.fuel_left)
