<sub>[← all labs](../../README.md)</sub>

# Pit strategy under caution risk (Monte Carlo)

> Cautions are random. Judge a strategy on its distribution of outcomes, not on one race.

`Python` · `NumPy`

**Companion to:**
- [Winning in NASCAR with AI/ML](https://www.linkedin.com/pulse/winning-nascar-aiml-tony-honesto-tkdvc/)
- [Motorsports competitive edge via AI use cases](https://www.linkedin.com/pulse/motorsports-competitive-edge-via-ai-use-cases-tony-honesto-d2j3c/)

## What it shows

- Simulates thousands of races with random cautions for two strategies: fixed fuel-window stops versus opportunistic stops under caution.
- Both strategies see the same random cautions, so the comparison is fair.
- Reports mean, 10th and 90th percentile race time, and shows the value of opportunism rising with the caution rate.

## Run it

```bash
bash labs/pit-strategy-monte-carlo/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
caution rate 0.01/lap: opportunistic saves  20.9 s on average (p90 fixed 177.9 min vs opportunistic 177.2 min)
caution rate 0.03/lap: opportunistic saves  47.3 s on average (p90 fixed 187.9 min vs opportunistic 186.9 min)
caution rate 0.06/lap: opportunistic saves  74.3 s on average (p90 fixed 199.8 min vs opportunistic 198.6 min)
```

## What's in here

| File | Purpose |
|---|---|
| `strategy.py` | Track parameters, race simulator and strategy comparison |
| `demo.py` | Compares the strategies at three caution rates |
| `tests/` | No-caution equivalence, rising value with cautions, fuel-window safety |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Fixed caution rate | Track- and lap-specific caution models learned from history |
| Simple pit loss | Pit-road speed, track position and wave-around rules |
| Two strategies | Optimisation over stop laps, tire sets and fuel-only stops |
