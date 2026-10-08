"""Event-time windowing for an out-of-order telemetry stream.

Radio links reorder and delay packets. Windows are keyed by *event time*, a
watermark (max event time seen minus allowed lateness) decides when a window is
final, and anything older than the watermark is diverted as late.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class WindowResult:
    car: str
    start_ms: int
    count: int
    max_speed: float
    avg_rpm: float


@dataclass
class TumblingWindows:
    size_ms: int = 1000
    lateness_ms: int = 500
    watermark_ms: int = -1
    _open: dict = field(default_factory=lambda: defaultdict(list))
    late: list = field(default_factory=list)

    def _start(self, ts: int) -> int:
        return ts - ts % self.size_ms

    def ingest(self, event: dict) -> list[WindowResult]:
        ts = event["ts_ms"]
        if ts < self.watermark_ms:
            self.late.append(event)            # too late: window already emitted
            return []
        self._open[(event["car"], self._start(ts))].append(event)
        self.watermark_ms = max(self.watermark_ms, ts - self.lateness_ms)
        return self._emit_ready()

    def _emit_ready(self) -> list[WindowResult]:
        ready = [k for k in self._open if k[1] + self.size_ms <= self.watermark_ms]
        return [self._close(k) for k in sorted(ready, key=lambda k: (k[1], k[0]))]

    def flush(self) -> list[WindowResult]:
        return [self._close(k) for k in sorted(self._open, key=lambda k: (k[1], k[0]))]

    def _close(self, key) -> WindowResult:
        evs = self._open.pop(key)
        return WindowResult(key[0], key[1], len(evs), max(e["speed"] for e in evs),
                            sum(e["rpm"] for e in evs) / len(evs))


def jittered_stream(seed: int = 4, cars=("5", "24"), seconds: int = 5, hz: int = 20):
    import random
    rng = random.Random(seed)
    events = []
    for car in cars:
        for i in range(seconds * hz):
            ts = i * (1000 // hz)
            events.append({"car": car, "ts_ms": ts, "speed": 180 + 20 * rng.random(),
                           "rpm": 9000 + 500 * rng.random(), "arrival": ts + rng.choice([5, 20, 60, 900])})
    return sorted(events, key=lambda e: e["arrival"])
