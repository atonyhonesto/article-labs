<sub>[← all labs](../../README.md)</sub>

# Parquet as a lightweight feature store

> Columnar, compressed and partitioned: read only the columns and the slices your model needs.

`Python` · `PyArrow` · `Parquet`

**Companion to:**
- [Parquet for Analytics & Feature Consumption](https://www.linkedin.com/pulse/parquet-analytics-feature-consumption-tony-honesto-oww7c/)

## What it shows

- Writing 200,000 feature rows as Parquet partitioned by season and series, compressed with zstd.
- Size on disk versus the same data as CSV.
- Building a training set with partition filters and column pruning, counting how many files were actually opened.
- Data types survive the round trip, unlike CSV.

## Run it

```bash
bash labs/parquet-feature-store/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output (from this lab's CI run):

```text
200,000 rows: CSV 13.9 MB vs Parquet (zstd) 5.3 MB in 9 partition files
Training slice (cup, 2025-26, 4 of 9 columns): 44,479 rows, opened 2 of 9 files
Dtypes preserved: {'tire_age': 'int16', 'fuel_kg': 'float32', 'track_temp_c': 'float32', 'lap_time_s': 'float32'}
```

## What's in here

| File | Purpose |
|---|---|
| `store.py` | Feature generation, partitioned write and filtered read (pyarrow) |
| `demo.py` | CSV vs. Parquet, then a training slice |
| `tests/` | Pruning, filtering and dtype tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Local folders | S3 / ADLS with a catalog (Glue, Unity Catalog) |
| pyarrow datasets | Feast, Databricks Feature Store or SageMaker Feature Store |
| Synthetic features | Features computed by the medallion pipeline |
