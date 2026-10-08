<sub>[← all labs](../../README.md)</sub>

# Medallion architecture in portable SQL

> Bronze keeps everything, silver keeps what's true, gold keeps what's useful. Replays shouldn't change any of it.

`Python` · `SQL` · `SQLite`

**Companion to:**
- [Snowflake and Databricks — Two Platforms, One Data Universe](https://www.linkedin.com/pulse/snowflake-databricks-two-platforms-one-data-universe-tony-honesto-nzyic/)
- [Google BigQuery](https://www.linkedin.com/pulse/google-bigquery-tony-honesto-w6fyc/)

## What it shows

- Bronze: every raw record appended with its batch id, nothing thrown away.
- Silver: typed, de-duplicated and validated with `ROW_NUMBER()`; bad rows go to a rejects table with a reason.
- Gold: per-car aggregates (laps, best lap, mean, lap-time variance) rebuilt from silver.
- Idempotency: a late correction updates silver, and replaying a whole batch changes nothing downstream.

## Run it

```bash
bash labs/medallion-sql/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
after batch 1: {'bronze_events': 8, 'silver_laps': 6, 'gold_car_summary': 2, 'dq_rejects': 2}
after a timing correction: {'bronze_events': 9, 'silver_laps': 6, 'gold_car_summary': 2, 'dq_rejects': 2}
after replaying batch 1 (late duplicate): {'bronze_events': 17, 'silver_laps': 6, 'gold_car_summary': 2, 'dq_rejects': 4}
  gold: ('24', 3, 30.95, 31.283)
  gold: ('5', 3, 31.0, 31.167)
  rejects: [('missing car',), ('implausible lap time',)]
```

## What's in here

| File | Purpose |
|---|---|
| `sql/silver.sql` | Clean, de-duplicate and validate |
| `sql/gold.sql` | Business aggregates |
| `pipeline.py` | Bronze load, rejects and batch runner (SQLite) |
| `demo.py` | Three batches including a correction and a replay |
| `tests/` | Idempotency and data-quality tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| SQLite | Snowflake, Databricks (Delta Lake) or BigQuery; the SQL is deliberately portable |
| Python runner | dbt models, Snowflake tasks or Databricks Workflows |
| Rejects table | Expectations (DLT, Great Expectations, dbt tests) with alerting |
