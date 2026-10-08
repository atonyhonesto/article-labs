<sub>[← all labs](../../README.md)</sub>

# Gradient-boosted forecasting, backtested properly

> A forecast that can't beat 'same day last week' isn't worth shipping.

`Python` · `scikit-learn` · `XGBoost-compatible`

**Companion to:**
- [Forecasting with XGBoost](https://www.linkedin.com/pulse/forecasting-xgboost-tony-honesto-pdwmc/)

## What it shows

- Lag, rolling and calendar features built only from the past.
- A rolling-origin backtest: train before a cutoff, forecast the next 7 days, move the cutoff, repeat.
- A naive seasonal baseline beside the model on every fold.
- XGBoost-compatible: swap in `XGBRegressor` and nothing else changes.

## Run it

```bash
bash labs/gradient-boosting-forecast/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Rolling-origin backtest, 7-day horizon (MAPE):
    cutoff  mape_model  mape_naive
2025-11-05        5.4%       10.1%
2025-11-12        7.2%       11.2%
2025-11-19        4.3%        4.3%
2025-11-26        4.1%        8.5%
2025-12-03        4.7%        7.0%
2025-12-10        3.8%        5.1%
2025-12-17        4.2%        3.4%
2025-12-24        4.1%        5.5%

Average: model 4.7% vs naive same-day-last-week 6.9%
```

## What's in here

| File | Purpose |
|---|---|
| `forecast.py` | Synthetic sales, feature builder and backtest |
| `demo.py` | Eight-fold backtest with MAPE per fold |
| `tests/` | Leakage and beats-baseline tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| One synthetic series | Thousands of series with hierarchy (store, product) |
| HistGradientBoosting | XGBoost/LightGBM with tuned hyper-parameters and prediction intervals |
| MAPE | Business-weighted error and bias tracking in production |
