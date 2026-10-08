<sub>[← all labs](../../README.md)</sub>

# An S3 telemetry lake with per-team access

> Every lap is a data event. Lay the keys out right and a prefix answers the question.

`Python` · `Amazon S3 pattern`

**Companion to:**
- [Amazon S3](https://www.linkedin.com/pulse/amazon-s3-tony-honesto-o8hmc/)

## What it shows

- Hive-style partitioned keys (`series=/season=/event=/session=/car=/lap=`) that sort and filter by prefix.
- Zero-padded lap numbers so lexical order equals lap order.
- A sync job that copies each team only its own cars, the pattern used to keep competitors' data apart.

## Run it

```bash
bash labs/s3-telemetry-lake/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Objects in lake: 20
Prefix query for car 24: 5 objects
Synced 15 objects to the team bucket; cars present: ['24', '48', '5']
```

## What's in here

| File | Purpose |
|---|---|
| `lake.py` | Key builder, a local bucket implementing put/get/list/copy, and the team sync |
| `demo.py` | Builds a 20-object lake, runs a prefix query and a team sync |
| `tests/` | Ordering, isolation and round-trip tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Local folder bucket | Amazon S3 (`put_object`, `list_objects_v2` with `Prefix`, `copy_object`) |
| Sync loop | S3 Replication rules or an EventBridge-triggered Lambda per new object |
| JSON per lap | Parquet per session, queryable with Athena via the Glue Data Catalog |
