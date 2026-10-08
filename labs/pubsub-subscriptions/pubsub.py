"""AppSync-style subscriptions in miniature.

In AWS AppSync a client subscribes to a mutation (e.g. `onLapCompleted(car: "24")`)
and the service pushes every matching mutation result to it over WebSockets.
The ideas that matter are reproduced here with asyncio queues:

* subscriptions carry argument filters; the server only fans out matches
* each subscriber has its own bounded queue, so one slow client can't stall the rest
* when a subscriber's queue is full, its oldest message is dropped and counted
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field


@dataclass
class Subscription:
    client: str
    field: str
    filters: dict
    queue: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(maxsize=50))
    dropped: int = 0

    def matches(self, field_name: str, payload: dict) -> bool:
        return field_name == self.field and all(payload.get(k) == v for k, v in self.filters.items())


class PubSub:
    def __init__(self):
        self.subs: list[Subscription] = []
        self.published = 0

    def subscribe(self, client: str, field_name: str, **filters) -> Subscription:
        sub = Subscription(client, field_name, filters)
        self.subs.append(sub)
        return sub

    def unsubscribe(self, sub: Subscription) -> None:
        self.subs.remove(sub)

    def mutate(self, field_name: str, payload: dict) -> int:
        """Apply a mutation and fan its result out. Returns how many subscribers received it."""
        self.published += 1
        delivered = 0
        for sub in self.subs:
            if sub.matches(field_name, payload):
                if sub.queue.full():
                    sub.queue.get_nowait()          # drop oldest: favour fresh data for live views
                    sub.dropped += 1
                sub.queue.put_nowait(payload)
                delivered += 1
        return delivered


async def drain(sub: Subscription) -> list[dict]:
    out = []
    while not sub.queue.empty():
        out.append(await sub.queue.get())
    return out
