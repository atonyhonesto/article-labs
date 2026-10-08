import json
import unittest
from pathlib import Path

import handlers

EVENTS = Path(__file__).resolve().parent.parent / "events"


class HandlerTests(unittest.TestCase):
    def setUp(self):
        self.store = handlers.IdempotencyStore()
        handlers.LEADERBOARD.clear()

    def test_duplicate_s3_notification_is_processed_once(self):
        out = handlers.on_file_landed(json.loads((EVENTS / "s3_put.json").read_text()), store=self.store)
        self.assertEqual(len(out["processed"]), 1)
        self.assertEqual(out["skipped_duplicates"], ["2026/results/race 42/official.csv"])

    def test_only_bad_messages_are_reported_for_retry(self):
        out = handlers.on_timing_batch(json.loads((EVENTS / "sqs_timing.json").read_text()), store=self.store)
        self.assertEqual({f["itemIdentifier"] for f in out["batchItemFailures"]}, {"m4", "m6"})

    def test_leaderboard_keeps_best_lap(self):
        handlers.on_timing_batch(json.loads((EVENTS / "sqs_timing.json").read_text()), store=self.store)
        self.assertEqual(handlers.LEADERBOARD["5"], {"laps": 2, "best_s": 30.987})
        self.assertEqual(handlers.LEADERBOARD["24"]["laps"], 1)


if __name__ == "__main__":
    unittest.main()
