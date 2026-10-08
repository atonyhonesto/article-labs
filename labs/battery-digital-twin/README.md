<sub>[← all labs](../../README.md)</sub>

# A battery digital twin that spots a failing cell

> A digital twin earns its keep the moment reality stops agreeing with it.

`Python` · `NumPy`

**Companion to:**
- [Elysia - Battery Management Software | Digital Twin Intelligence](https://www.linkedin.com/pulse/elysia-battery-management-software-digital-twin-tony-honesto-adm1c/)

## What it shows

- A first-order equivalent-circuit model (open-circuit voltage, series resistance, one RC pair) plus a lumped thermal model.
- Coulomb counting for state of charge as the twin follows a drive cycle.
- A rolling residual monitor: compare measured voltage with the twin's prediction and alert when they drift apart.
- A healthy cell tracks within a few millivolts; an aged cell with higher resistance trips the alert in two minutes.

## Run it

```bash
bash labs/battery-digital-twin/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
healthy cell: SOC 0.43, max temp 27.4 °C, mean |V error| 2.4 mV -> tracking the twin
aged cell   : SOC 0.43, max temp 28.8 °C, mean |V error| 69.8 mV -> ALERT at 120 s
```

## What's in here

| File | Purpose |
|---|---|
| `twin.py` | Cell model, drive cycle and residual monitor |
| `demo.py` | Healthy vs. aged cell against the same twin |
| `tests/` | SOC, thermal and alert tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic drive cycle | Live current, voltage and temperature from the BMS over CAN |
| Fixed parameters | Parameters fitted from lab characterisation and updated as the cell ages (Kalman filter) |
| Single cell | Pack-level twin with cell balancing and per-module thermal models |
