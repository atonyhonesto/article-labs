<sub>[← all labs](../../README.md)</sub>

# AWS Lambda handlers for race-weekend events

> The fastest code in racing might be the code that only runs when it has to.

`Python` · `AWS Lambda pattern`

**Companion to:**
- [AWS Lambda](https://www.linkedin.com/pulse/aws-lambda-tony-honesto-5risc/)

## What it shows

- An S3 `ObjectCreated` handler for results files landing from the tech shed, deduplicating repeated notifications.
- An SQS handler for timing-loop crossings that returns `batchItemFailures`, so only bad messages are retried.
- Idempotency on every handler: Lambda and its triggers deliver at least once, so repeats must be harmless.
- Event fixtures in `events/` use the real AWS shapes, so the handlers deploy unchanged.

## Run it

```bash
bash labs/lambda-race-events/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
S3 trigger  -> {"processed": [{"bucket": "race-weekend-raw", "key": "2026/results/race 42/official.csv", "kind": "results"}], "skipped_duplicates": ["2026/results/race 42/official.csv"]}
SQS trigger -> {"batchItemFailures": [{"itemIdentifier": "m4"}, {"itemIdentifier": "m6"}]}
Leaderboard -> {"24": {"best_s": 31.204, "laps": 1}, "5": {"best_s": 30.987, "laps": 2}}
```

## What's in here

| File | Purpose |
|---|---|
| `handlers.py` | Both handlers, an idempotency store and a tiny leaderboard |
| `events/` | S3 and SQS event fixtures |
| `demo.py` | Replays the fixtures through the handlers |
| `tests/` | Duplicate, partial-failure and leaderboard tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| In-memory idempotency set | DynamoDB conditional writes (or Powertools Idempotency) |
| In-memory leaderboard | DynamoDB / ElastiCache, pushed to clients via AppSync or WebSockets |
| Local fixtures | S3 event notifications and an SQS event source mapping with ReportBatchItemFailures |
