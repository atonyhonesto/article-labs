<sub>[← all labs](../../README.md)</sub>

# Stint pace analyzer (FastF1-style)

> Raw lap times lie. In-laps, out-laps, safety cars, fuel load and tire age all have to come out before drivers can be compared.

`Python` · `pandas`

**Companion to:**
- [F1 Lap Time Analyzer — Python, Streamlit & FastF1 in Action](https://www.linkedin.com/pulse/f1-lap-time-analyzer-python-streamlit-fastf1-action-tony-honesto-qlmgc/)
- [ATLAS Data-Driven Race Strategy](https://www.linkedin.com/pulse/atlas-data-driven-race-strategy-tony-honesto-5s2gc/)

## What it shows

- Splits laps into stints and drops pit laps and safety-car laps.
- Corrects for fuel burn and for tire age (estimated from the data), then compares drivers on median pace.
- Shows why the tire-age correction matters: a driver on more, shorter stints looks faster on fresher rubber.

## Run it

```bash
bash labs/stint-pace-analyzer/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Race pace corrected for fuel and tire age (green-flag laps only):
        median_s  std_s  laps_used  gap_s
Driver                                   
AAA       89.980  0.144         48  0.000
BBB       90.249  0.172         50  0.269
CCC       90.433  0.148         48  0.453

Median tire degradation: 0.063 s/lap across 8 stints
```

## What's in here

| File | Purpose |
|---|---|
| `pace.py` | Synthetic session, representative-lap filter, degradation estimate, driver pace |
| `demo.py` | Prints corrected pace and degradation |
| `tests/` | Filtering, driver order and degradation tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic session | `fastf1.get_session(...).laps`, same column names |
| Fixed fuel effect | Team-specific fuel-effect estimates |
| Printed tables | A Streamlit dashboard with lap and stint charts |
