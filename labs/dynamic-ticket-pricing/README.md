<sub>[← all labs](../../README.md)</sub>

# Dynamic ticket pricing with guardrails

> Learn how each section responds to price, then move prices only as far as fans will tolerate.

`Python` · `NumPy`

**Companion to:**
- [ML Pipelines Powering Dynamic Ticket Pricing](https://www.linkedin.com/pulse/ml-pipelines-powering-dynamic-ticket-pricing-tony-honesto-8kcrc/)

## What it shows

- Fits a constant-elasticity demand curve per section from past sales.
- Chooses the revenue-maximising price, counting only seats that are actually left.
- Enforces a floor, a ceiling and a maximum change per update.

## Run it

```bash
bash labs/dynamic-ticket-pricing/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Lower bowl : elasticity -1.40 (true -1.4)  $140 -> $150  expected revenue $56,000 -> $59,977
Upper deck : elasticity -2.30 (true -2.3)  $60 -> $56  expected revenue $129,142 -> $140,000
```

## What's in here

| File | Purpose |
|---|---|
| `pricing.py` | Elasticity fit, demand model and constrained price search |
| `demo.py` | Prices a lower-bowl and an upper-deck section |
| `tests/` | Elasticity recovery, guardrails and sell-out tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic sales history | Transaction history plus opponent, day, weather and resale signals |
| Constant elasticity | Time-to-event demand curves and secondary-market feedback |
| Grid search | Optimisation across sections with inventory and fairness constraints |
