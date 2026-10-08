"""The parts of Apache Kafka that decide correctness, in one file.

* A topic is a set of append-only partitions; a record's key picks its partition,
  so all events for one car stay in order.
* A consumer group splits partitions among its members; each partition has
  exactly one owner in the group at a time.
* Consumers commit offsets. After a crash, the new owner resumes from the last
  COMMITTED offset, so anything processed but not committed is processed again
  (at-least-once). Idempotent handlers make that harmless.
"""
from __future__ import annotations

import zlib
from dataclasses import dataclass, field


@dataclass
class Topic:
    name: str
    partitions: int
    log: list = field(default_factory=list)

    def __post_init__(self):
        self.log = [[] for _ in range(self.partitions)]

    def produce(self, key: str, value: dict) -> tuple[int, int]:
        p = zlib.crc32(key.encode()) % self.partitions       # Kafka uses murmur2; any stable hash shows the idea
        self.log[p].append((key, value))
        return p, len(self.log[p]) - 1


@dataclass
class ConsumerGroup:
    topic: Topic
    members: list[str] = field(default_factory=list)
    committed: dict = field(default_factory=dict)            # partition -> next offset to read
    assignment: dict = field(default_factory=dict)
    rebalances: int = 0

    def join(self, member: str) -> None:
        self.members.append(member)
        self._rebalance()

    def leave(self, member: str) -> None:
        self.members.remove(member)
        self._rebalance()

    def _rebalance(self) -> None:
        """Range-style assignment: spread partitions across members as evenly as possible."""
        self.rebalances += 1
        self.assignment = {m: [] for m in self.members}
        for p in range(self.topic.partitions):
            if self.members:
                self.assignment[self.members[p % len(self.members)]].append(p)

    def poll(self, member: str, max_records: int = 10) -> list[tuple[int, int, str, dict]]:
        out = []
        for p in self.assignment.get(member, []):
            start = self.committed.get(p, 0)
            for off in range(start, min(start + max_records, len(self.topic.log[p]))):
                k, v = self.topic.log[p][off]
                out.append((p, off, k, v))
        return out

    def commit(self, records: list[tuple[int, int, str, dict]]) -> None:
        for p, off, _, _ in records:
            self.committed[p] = max(self.committed.get(p, 0), off + 1)

    def lag(self) -> int:
        return sum(len(self.topic.log[p]) - self.committed.get(p, 0) for p in range(self.topic.partitions))
