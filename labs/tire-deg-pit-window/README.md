<sub>[← all labs](../../README.md)</sub>

# Tire degradation → pit window

> Every strategy call on the pit wall is a prediction. This one learns how fast the tires fall off, then picks the lap to stop.

`Python` · `scikit-learn` · `pandas`

**Companion to:**
- [Python Machine Learning in Motorsports](https://www.linkedin.com/pulse/python-machine-learning-motorsports-tony-honesto-aqmmc/)

## What it shows

- Fits a polynomial model of lap time from tire age, track temperature and fuel load (scikit-learn pipeline).
- Simulates a one-stop race for every candidate pit lap and returns the fastest, including the time lost in the pit lane.
- Tests check the model learns real fall-off, the optimum sits inside the window, and the pit loss is counted exactly once.

## Run it

```bash
bash labs/tire-deg-pit-window/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Trained on 1200 practice laps from 40 stints
Track 28°C: pit on lap 24  race time 77.67 min  (15.9 s faster than the worst lap in the window)
Track 42°C: pit on lap 24  race time 77.85 min  (19.0 s faster than the worst lap in the window)
```

## What's in here

| File | Purpose |
|---|---|
| `pitwindow.py` | Synthetic practice data, degradation model, race-time simulator, pit-lap search |
| `demo.py` | Trains on 1,200 laps and recommends a pit lap at two track temperatures |
| `tests/` | Behaviour tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic practice stints | Timing and telemetry from practice sessions |
| Quadratic fall-off model | Compound-specific models, plus traffic and track evolution |
| One-stop search | Multi-stop strategy tree with caution probabilities (see `pit-strategy-monte-carlo`) |
