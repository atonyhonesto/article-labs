"""ITIL-style priority and SLA clocks, the logic every ITSM platform runs underneath.

* Priority comes from impact x urgency (a standard 3x3 matrix), not from how loud the caller is.
* Each priority has response and resolution targets.
* P1 runs 24x7; lower priorities only count business hours (Mon-Fri 08:00-18:00).
* The clock pauses while the ticket is "awaiting customer".
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

MATRIX = {  # (impact, urgency) -> priority, 1 = high
    (1, 1): "P1", (1, 2): "P2", (1, 3): "P3",
    (2, 1): "P2", (2, 2): "P3", (2, 3): "P4",
    (3, 1): "P3", (3, 2): "P4", (3, 3): "P5",
}
TARGETS = {  # priority -> (resolution target, 24x7?)
    "P1": (timedelta(hours=4), True), "P2": (timedelta(hours=8), False), "P3": (timedelta(hours=24), False),
    "P4": (timedelta(hours=40), False), "P5": (timedelta(hours=80), False),
}
BUSINESS_START, BUSINESS_END = 8, 18


def priority(impact: int, urgency: int) -> str:
    return MATRIX[(impact, urgency)]


def counted_time(start: datetime, end: datetime, around_the_clock: bool) -> timedelta:
    """Time between start and end that counts toward the SLA."""
    if end <= start:
        return timedelta(0)
    if around_the_clock:
        return end - start
    total, t = timedelta(0), start
    while t < end:
        day_open = t.replace(hour=BUSINESS_START, minute=0, second=0, microsecond=0)
        day_close = t.replace(hour=BUSINESS_END, minute=0, second=0, microsecond=0)
        if t.weekday() < 5:
            lo, hi = max(t, day_open), min(end, day_close)
            if hi > lo:
                total += hi - lo
        t = (t + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return total


@dataclass
class Ticket:
    opened: datetime
    impact: int
    urgency: int
    events: list = field(default_factory=list)      # (time, status)

    @property
    def priority(self) -> str:
        return priority(self.impact, self.urgency)

    def elapsed(self, now: datetime) -> timedelta:
        """SLA time used, excluding 'awaiting customer' periods."""
        target, always = TARGETS[self.priority]
        timeline = [(self.opened, "in progress")] + sorted(self.events) + [(now, "now")]
        used = timedelta(0)
        for (t0, status), (t1, _) in zip(timeline, timeline[1:]):
            if status != "awaiting customer":
                used += counted_time(t0, min(t1, now), always)
        return used

    def status(self, now: datetime) -> tuple[str, float]:
        target, _ = TARGETS[self.priority]
        pct = self.elapsed(now) / target
        return ("BREACHED" if pct >= 1 else "AT RISK" if pct >= 0.75 else "OK"), pct
