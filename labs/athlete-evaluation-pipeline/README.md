<sub>[← all labs](../../README.md)</sub>

# An athlete-evaluation ML pipeline

> If preprocessing happens outside the model, cross-validation quietly lies.

`Python` · `scikit-learn`

**Companion to:**
- [ML Pipelines for Athlete Evaluation](https://www.linkedin.com/pulse/ml-pipelines-athlete-evaluation-tony-honesto-q1vsc/)

## What it shows

- A single scikit-learn `Pipeline`: median imputation and scaling for numbers, one-hot encoding for categories, then a logistic model.
- Every step is fitted inside each CV fold, so nothing about validation athletes leaks into training.
- Scores new prospects with missing combine data and a position the model has never seen.

## Run it

```bash
bash labs/athlete-evaluation-pipeline/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
1200 prospects, 30% made a roster, 38% missing some combine data
Cross-validated ROC AUC: 0.929
  WR from G5, 40yd 4.38s -> roster probability 97%
  TE from FCS, 40yd 4.85s -> roster probability 0%
```

## What's in here

| File | Purpose |
|---|---|
| `pipeline.py` | Synthetic prospects, the pipeline and cross-validated AUC |
| `demo.py` | Reports AUC and scores two new prospects |
| `tests/` | AUC floor and unseen-category/missing-value tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic combine and stats | Tracking data, game film features and scouting grades |
| Roster outcome label | Longer-horizon outcomes such as snaps played or contract value |
| Logistic model | Calibrated gradient boosting, with fairness and drift monitoring |
