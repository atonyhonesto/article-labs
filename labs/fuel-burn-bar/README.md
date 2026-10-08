<sub>[← all labs](../../README.md)</sub>

# A broadcast fuel 'burn bar'

> Is this car burning fuel faster than it can afford? One gauge, updated every lap.

`Python` · `stdlib`

**Companion to:**
- [Amazon Prime Video: Burn Bar, Tech behind the display](https://www.linkedin.com/pulse/amazon-prime-video-burn-bar-tech-behind-display-tony-honesto-p6mgc/)
- [Prime Vision + Next Gen Stats](https://www.linkedin.com/pulse/prime-vision-next-gen-stats-tony-honesto-7yt8c/)

## What it shows

- Computes the fuel-per-lap target from fuel left and laps left.
- Uses a rolling average that ignores caution laps, so slow laps don't flatter the number.
- Renders an ASCII gauge with SAVE FUEL / ON TARGET / CAN PUSH states.

## Run it

```bash
bash labs/fuel-burn-bar/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
lap  5  avg 1.95 kg vs target 1.89  [----------|-#--------]  +3.1%  SAVE FUEL
lap 12  avg 1.95 kg vs target 1.88  [----------|-#--------]  +3.6%  SAVE FUEL
lap 15  avg 1.95 kg vs target 1.93  [----------|#---------]  +1.2%  ON TARGET
lap 30  avg 1.92 kg vs target 1.93  [----------|----------]  -0.5%  ON TARGET
lap 45  avg 1.80 kg vs target 2.08  [---#------|----------] -13.5%  CAN PUSH
lap 55  avg 1.80 kg vs target 3.02  [#---------|----------] -40.3%  CAN PUSH
Finished with 3.6 kg to spare
```

## What's in here

| File | Purpose |
|---|---|
| `burnbar.py` | Reading, rolling average, target and gauge |
| `demo.py` | A 58-lap race with a caution |
| `tests/` | State, caution and gauge tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Reported fuel per lap | Fuel-flow sensor telemetry at high frequency |
| ASCII bar | Broadcast graphics engine driven by the live feed |
| Single car | Every car, plus pit-window predictions |
