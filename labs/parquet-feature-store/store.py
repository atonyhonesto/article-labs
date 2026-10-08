"""Parquet as a feature store for model training.

* Write features partitioned by season and series (Hive-style folders), so a
  training job for one series never opens the others' files.
* Read only the columns the model needs (columnar format: the rest are never read).
* Push filters down, so row groups whose min/max statistics rule them out are skipped.
* Types survive the round trip (unlike CSV), and the files are far smaller.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq


def features(rows: int = 200_000, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "season": rng.choice([2024, 2025, 2026], rows),
        "series": rng.choice(["cup", "xfinity", "truck"], rows),
        "car": rng.integers(1, 99, rows).astype("int16"),
        "lap": rng.integers(1, 400, rows).astype("int16"),
        "tire_age": rng.integers(0, 60, rows).astype("int16"),
        "fuel_kg": rng.uniform(0, 80, rows).astype("float32"),
        "track_temp_c": rng.uniform(15, 55, rows).astype("float32"),
        "lap_time_s": rng.normal(31, 1.2, rows).astype("float32"),
        "session_ts": pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 10**7, rows), unit="s"),
    })


def write(df: pd.DataFrame, root: Path) -> None:
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_to_dataset(table, root_path=str(root), partition_cols=["season", "series"],
                        compression="zstd", row_group_size=20_000)


def training_set(root: Path, series: str, seasons: list[int], columns: list[str]) -> tuple[pd.DataFrame, int]:
    """Return the requested slice and how many files were actually opened."""
    dataset = ds.dataset(str(root), format="parquet", partitioning="hive")
    flt = (ds.field("series") == series) & ds.field("season").isin(seasons)
    fragments = list(dataset.get_fragments(filter=flt))
    table = dataset.to_table(columns=columns, filter=flt)
    return table.to_pandas(), len(fragments)


def size_on_disk(path: Path) -> int:
    return sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())
