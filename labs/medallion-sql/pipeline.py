"""A medallion (bronze -> silver -> gold) pipeline in portable SQL.

The same three layers exist on Snowflake, Databricks and BigQuery; only the
dialect details change. SQLite stands in so the lab runs anywhere, and the SQL
sticks to window functions, upserts and JSON extraction that all three support
in some form.

* Bronze: raw JSON exactly as received, tagged with a batch id. Never edited.
* Silver: typed, deduplicated (latest record per key wins), validated.
* Gold: aggregates for dashboards, rebuilt from silver.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

SQL = Path(__file__).with_name("sql")

DDL = """
CREATE TABLE IF NOT EXISTS bronze_events (batch_id TEXT, received_at TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS silver_laps (
    race_id TEXT, car TEXT, lap INTEGER, lap_time_s REAL, recorded_at TEXT,
    PRIMARY KEY (race_id, car, lap));
CREATE TABLE IF NOT EXISTS gold_car_summary (
    race_id TEXT, car TEXT, laps INTEGER, best_lap_s REAL, avg_lap_s REAL, lap_time_variance REAL);
CREATE TABLE IF NOT EXISTS dq_rejects (batch_id TEXT, payload TEXT, reason TEXT);
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.executescript(DDL)
    return con


def load_bronze(con, batch_id: str, records: list[dict]) -> None:
    con.executemany("INSERT INTO bronze_events VALUES (?, datetime('now'), ?)",
                    [(batch_id, json.dumps(r)) for r in records])


def record_rejects(con, batch_id: str) -> None:
    con.execute("""
        INSERT INTO dq_rejects
        SELECT batch_id, payload,
               CASE WHEN json_extract(payload, '$.car') IS NULL OR TRIM(json_extract(payload, '$.car')) = '' THEN 'missing car'
                    ELSE 'implausible lap time' END
        FROM bronze_events
        WHERE batch_id = ? AND (
              json_extract(payload, '$.car') IS NULL OR TRIM(json_extract(payload, '$.car')) = ''
              OR CAST(json_extract(payload, '$.lap_time_s') AS REAL) NOT BETWEEN 20 AND 300)""", (batch_id,))


def run_batch(con, batch_id: str, records: list[dict]) -> dict:
    load_bronze(con, batch_id, records)
    record_rejects(con, batch_id)
    con.execute((SQL / "silver.sql").read_text(), {"batch_id": batch_id})
    con.executescript((SQL / "gold.sql").read_text())
    con.commit()
    return {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in ("bronze_events", "silver_laps", "gold_car_summary", "dq_rejects")}
