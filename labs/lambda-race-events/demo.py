import json
from pathlib import Path

import handlers

here = Path(__file__).parent
s3 = handlers.on_file_landed(json.loads((here / "events/s3_put.json").read_text()))
print("S3 trigger  ->", json.dumps(s3))
sqs = handlers.on_timing_batch(json.loads((here / "events/sqs_timing.json").read_text()))
print("SQS trigger ->", json.dumps(sqs))
print("Leaderboard ->", json.dumps(handlers.LEADERBOARD, sort_keys=True))
