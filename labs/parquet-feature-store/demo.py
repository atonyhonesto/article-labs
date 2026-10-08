import tempfile
from pathlib import Path

from store import features, size_on_disk, training_set, write

df = features()
with tempfile.TemporaryDirectory() as tmp:
    root, csv = Path(tmp) / "features", Path(tmp) / "features.csv"
    write(df, root)
    df.to_csv(csv, index=False)
    total_files = len(list(root.rglob("*.parquet")))
    print(f"{len(df):,} rows: CSV {size_on_disk(csv) / 1e6:.1f} MB vs Parquet (zstd) {size_on_disk(root) / 1e6:.1f} MB "
          f"in {total_files} partition files")
    cols = ["tire_age", "fuel_kg", "track_temp_c", "lap_time_s"]
    train, opened = training_set(root, "cup", [2025, 2026], cols)
    print(f"Training slice (cup, 2025-26, {len(cols)} of {df.shape[1]} columns): {len(train):,} rows, "
          f"opened {opened} of {total_files} files")
    print("Dtypes preserved:", dict(train.dtypes.astype(str)))
