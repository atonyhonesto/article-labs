"""Lambda-style handlers for a race weekend, runnable locally with event fixtures.

The shapes follow the real AWS event formats (S3 Put notifications, SQS batches)
so the same functions deploy unchanged behind those triggers.
"""
from __future__ import annotations

import json
import urllib.parse


class IdempotencyStore:
    """Stand-in for a DynamoDB conditional put: remembers processed event IDs."""

    def __init__(self):
        self._seen: set[str] = set()

    def claim(self, key: str) -> bool:
        if key in self._seen:
            return False
        self._seen.add(key)
        return True


STORE = IdempotencyStore()
LEADERBOARD: dict[str, dict] = {}


def on_file_landed(event: dict, context=None, store: IdempotencyStore = STORE) -> dict:
    """S3 Put trigger: a results file landed from the tech shed."""
    processed, skipped = [], []
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        etag = record["s3"]["object"].get("eTag", "")
        if not store.claim(f"{bucket}/{key}#{etag}"):
            skipped.append(key)            # S3 can deliver the same notification twice
            continue
        processed.append({"bucket": bucket, "key": key, "kind": key.split("/")[1]})
    return {"processed": processed, "skipped_duplicates": skipped}


def on_timing_batch(event: dict, context=None, store: IdempotencyStore = STORE) -> dict:
    """SQS trigger: a batch of timing-loop crossings.

    Returns `batchItemFailures` so only the bad messages are retried, not the whole batch.
    """
    failures = []
    for msg in event.get("Records", []):
        try:
            crossing = json.loads(msg["body"])
            car, lap, t = crossing["car"], int(crossing["lap"]), float(crossing["time_s"])
            if lap < 1 or t <= 0:
                raise ValueError("bad lap or time")
        except (KeyError, ValueError, json.JSONDecodeError):
            failures.append({"itemIdentifier": msg["messageId"]})
            continue
        if not store.claim(f"crossing:{car}:{lap}"):
            continue                        # at-least-once delivery: ignore repeats
        best = LEADERBOARD.setdefault(car, {"laps": 0, "best_s": None})
        best["laps"] = max(best["laps"], lap)
        best["best_s"] = t if best["best_s"] is None else min(best["best_s"], t)
    return {"batchItemFailures": failures}
