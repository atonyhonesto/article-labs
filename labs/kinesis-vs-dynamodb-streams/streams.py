"""Kinesis Data Streams vs DynamoDB Streams, as two small simulations.

Both are ordered, sharded logs, but they answer different questions:

| | Kinesis Data Streams | DynamoDB Streams |
|---|---|---|
| What goes in | any record you put | item-level changes to one table |
| Ordering | per partition key, within a shard | per item key |
| Retention | 24 h default, up to 365 days | 24 h, fixed |
| Readers | many consumers, each with its own checkpoint | Lambda/KCL readers (2 recommended per shard) |
| Record content | your payload | KEYS_ONLY / NEW_IMAGE / OLD_IMAGE / NEW_AND_OLD_IMAGES |

The simulations show ordering by key, per-consumer checkpoints and the
"old vs new image" records that make DynamoDB Streams good for change data capture.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


def shard_for(key: str, shards: int) -> int:
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % shards     # Kinesis hashes the partition key (MD5)


@dataclass
class KinesisStream:
    shards: int = 4
    retention_s: int = 24 * 3600
    _log: list = field(default_factory=list)
    checkpoints: dict = field(default_factory=dict)

    def __post_init__(self):
        self._log = [[] for _ in range(self.shards)]

    def put_record(self, partition_key: str, data: dict, ts: int) -> tuple[int, int]:
        s = shard_for(partition_key, self.shards)
        seq = len(self._log[s])
        self._log[s].append({"seq": seq, "key": partition_key, "data": data, "ts": ts})
        return s, seq

    def expire(self, now: int) -> None:
        self._log = [[r for r in shard if now - r["ts"] < self.retention_s] for shard in self._log]

    def read(self, consumer: str, shard: int, limit: int = 100) -> list[dict]:
        """Each consumer reads from its own checkpoint, so many applications can read the same data."""
        start = self.checkpoints.get((consumer, shard), -1)
        recs = [r for r in self._log[shard] if r["seq"] > start][:limit]
        if recs:
            self.checkpoints[(consumer, shard)] = recs[-1]["seq"]
        return recs


@dataclass
class DynamoTableWithStream:
    view: str = "NEW_AND_OLD_IMAGES"
    items: dict = field(default_factory=dict)
    stream: list = field(default_factory=list)

    def put_item(self, key: str, item: dict) -> None:
        old = self.items.get(key)
        self.items[key] = item
        self._emit("MODIFY" if old else "INSERT", key, old, item)

    def delete_item(self, key: str) -> None:
        old = self.items.pop(key, None)
        if old is not None:
            self._emit("REMOVE", key, old, None)

    def _emit(self, event: str, key: str, old, new) -> None:
        rec = {"eventName": event, "Keys": {"id": key}}
        if self.view in ("NEW_IMAGE", "NEW_AND_OLD_IMAGES") and new is not None:
            rec["NewImage"] = new
        if self.view in ("OLD_IMAGE", "NEW_AND_OLD_IMAGES") and old is not None:
            rec["OldImage"] = old
        self.stream.append(rec)


def changed_fields(record: dict) -> dict:
    """What changed in a MODIFY, the question CDC consumers usually ask."""
    old, new = record.get("OldImage", {}), record.get("NewImage", {})
    return {k: (old.get(k), new.get(k)) for k in set(old) | set(new) if old.get(k) != new.get(k)}
