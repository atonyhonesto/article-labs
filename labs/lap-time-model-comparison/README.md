<sub>[← all labs](../../README.md)</sub>

# Comparing ML models for lap-time prediction

> The model that wins on a random split isn't always the one that wins on a new stint.

`Python` · `scikit-learn`

**Companion to:**
- [Machine Learning Approaches for Motorsports Competitive Advantage](https://www.linkedin.com/pulse/machine-learning-approaches-motorsports-competitive-tony-honesto-agstc/)

## What it shows

- Ridge regression, random forest and gradient boosting on the same features.
- Grouped cross-validation (whole stints held out) versus a random split, and how the random split flatters every model.
- Why tree models win here: soft tires fall off a cliff after 16 laps, a non-linearity a linear model can't capture.

## Run it

```bash
bash labs/lap-time-model-comparison/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
1500 laps, 60 stints. Mean absolute error in seconds:
            model  mae_grouped_s  mae_random_split_s
gradient_boosting          0.275               0.144
    random_forest          0.285               0.157
            ridge          0.474               0.471

Best on unseen stints: gradient_boosting
```

## What's in here

| File | Purpose |
|---|---|
| `compare.py` | Synthetic stints, the three models, grouped and random cross-validation |
| `demo.py` | Prints mean absolute error per model |
| `tests/` | Checks the tree model wins and that random splits look optimistic |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic stints | Practice and race laps with weather, traffic and setup data |
| Three model families | Plus feature engineering, hyper-parameter search and per-track models |
| Offline CV | Backtesting against previous race weekends |
