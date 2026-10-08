<sub>[← all labs](../../README.md)</sub>

# Hybrid energy budget with and without the MGU-H

> Take away exhaust-heat recovery and every joule has to come from braking.

`Python` · `stdlib`

**Companion to:**
- [MGU-H Removed from F1 Power Units in 2026](https://www.linkedin.com/pulse/mgu-h-removed-from-f1-power-units-2026-tony-honesto-oahtc/)

## What it shows

- Simulates battery state of charge through braking zones, corners and straights.
- Finds the highest deployment level a car can sustain lap after lap.
- Compares a pre-2026-style unit (with MGU-H) to a 2026-style unit (bigger MGU-K, no MGU-H).

## Run it

```bash
bash labs/ers-energy-budget/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
with MGU-H (pre-2026)         : can deploy 60.7% of full MGU-K power on every straight, 1.89 MJ per lap without draining the battery
no MGU-H, 350 kW MGU-K (2026) : can deploy 10.7% of full MGU-K power on every straight, 0.98 MJ per lap without draining the battery
```

## What's in here

| File | Purpose |
|---|---|
| `ers.py` | Lap segments, power-unit model, lap simulation and sustainable-deployment search |
| `demo.py` | Compares the two power-unit types |
| `tests/` | Battery-limit, MGU-H and depletion tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Illustrative power and battery numbers | Regulation limits on harvest, deployment and state-of-charge window |
| Segment-level lap | Distance-based simulation with speed-dependent deployment |
| Flat deployment | Optimised deployment maps per straight |
