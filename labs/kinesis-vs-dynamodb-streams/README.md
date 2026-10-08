<sub>[← all labs](../../README.md)</sub>

# Kinesis Data Streams vs. DynamoDB Streams

> Both are ordered streams of records. One carries the events you send; the other carries the changes to your table.

`Python` · `stdlib`

**Companion to:**
- [Amazon Kinesis Streams vs DynamoDB Streams](https://www.linkedin.com/pulse/amazon-kinesis-streams-vs-dynamodb-tony-honesto-ble7c/)

## What it shows

- Kinesis: partition key → shard by hash, so one car's laps stay in order on one shard.
- Independent consumers each keep their own checkpoint and re-read the same records.
- Retention: records expire after 24 hours unless you extend it.
- DynamoDB Streams: INSERT / MODIFY / REMOVE records with old and new images, so a consumer can see exactly what changed.

## Run it

```bash
bash labs/kinesis-vs-dynamodb-streams/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Kinesis: car 24 laps in order on shard 1 -> [1, 2, 3]
         a second consumer reads the same records from its own checkpoint: 5 records
         after 24 h retention, records left: 2
DynamoDB stream: ['INSERT', 'MODIFY', 'REMOVE']
  MODIFY changed: {'position': (3, 1)}
```

## What's in here

| File | Purpose |
|---|---|
| `streams.py` | Shard hashing, checkpoints, retention and a table with a change stream |
| `demo.py` | Same race data through both |
| `tests/` | Ordering, fan-out, retention and change-record tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| MD5 shard hash in Python | Kinesis hashes partition keys with MD5 across shard key ranges |
| In-memory checkpoints | KCL leases in DynamoDB, or Lambda event source mappings |
| Simulated stream view | `NEW_AND_OLD_IMAGES` stream view type on the table |
