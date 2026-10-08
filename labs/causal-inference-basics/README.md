<sub>[← all labs](../../README.md)</sub>

# Causal inference: did the upgrade make us faster?

> Teams that bought the upgrade were already faster. The raw comparison mostly measures their budgets.

`Python` · `NumPy` · `scikit-learn`

**Companion to:**
- [Statistics: Causal Inference](https://www.linkedin.com/pulse/statistics-causal-inference-tony-honesto-6bkyc/)

## What it shows

- A confounded dataset where the naive difference in means is about 4× the true effect.
- Regression adjustment: control for the confounder in a linear model.
- Inverse propensity weighting: model who adopts, then reweight so both groups look alike.
- Tests check the naive estimate is biased and both adjustments recover the truth.

## Run it

```bash
bash labs/causal-inference-basics/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
True effect of the aero package:   -0.200 s/lap
Naive difference in means:          -0.825 s/lap  <- budget confounds it
Regression adjustment for budget:   -0.189 s/lap
Inverse propensity weighting:       -0.186 s/lap
```

## What's in here

| File | Purpose |
|---|---|
| `causal.py` | Simulation, naive estimate, regression adjustment, IPW |
| `demo.py` | Prints all three estimates against the truth |
| `tests/` | Bias and recovery tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| One known confounder | Many, partly unobserved: use domain knowledge and a causal diagram |
| Simple models | Doubly robust estimators, matching, or difference-in-differences |
| Simulated truth | No ground truth: sensitivity analysis instead |
