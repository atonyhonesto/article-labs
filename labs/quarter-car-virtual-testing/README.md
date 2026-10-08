<sub>[← all labs](../../README.md)</sub>

# Virtual testing with a quarter-car model

> Test the damper before you build it. A two-mass model shows the ride-versus-grip trade-off a rig would.

`Python` · `SciPy` · `ODE simulation`

**Companion to:**
- [Virtual Testing with MSC Adams](https://www.linkedin.com/pulse/virtual-testing-msc-adams-tony-honesto-wwq4c/)
- [Helmut Schmidt University - Vehicle Dynamics Certificate](https://www.linkedin.com/pulse/helmut-schmidt-university-vehicle-dynamics-tony-honesto-lanoc/)
- [MATLAB and Simulink](https://www.linkedin.com/pulse/matlab-simulink-tony-honesto-ltrfc/)

## What it shows

- The quarter-car equations (body, wheel, suspension spring and damper, tyre spring) solved with SciPy.
- Two test inputs: a speed bump and a random rough road.
- A damping sweep scored on comfort (body acceleration), road holding (tyre load variation) and suspension travel.
- The trade-off: soft damping rides well but lets the wheel hop, stiff damping holds the road but hits harder.

## Run it

```bash
bash labs/quarter-car-virtual-testing/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Quarter car: body mode 1.39 Hz, critical damping 5,477 N·s/m

50 mm x 2 m speed bump at 36 km/h
  damping  c (N·s/m)  comfort (m/s² RMS)  tyre load var (% RMS)  travel (mm)  contact
     10%        548               1.221                   11.6         43.6  ok
     20%      1,095               1.124                   10.5         41.0  ok
     30%      1,643               1.241                   11.8         38.7  ok
     45%      2,465               1.537                   15.1         35.7  ok
     70%      3,834               2.096                   21.0         34.8  ok
    100%      5,477               2.742                   27.7         33.3  LOST
  best comfort at 20% of critical damping, steadiest tyre load at 20%

rough road at 90 km/h
  damping  c (N·s/m)  comfort (m/s² RMS)  tyre load var (% RMS)  travel (mm)  contact
     10%        548               0.470                   12.5         15.4  ok
     20%      1,095               0.455                    9.3         12.8  ok
     30%      1,643               0.497                    8.3         11.1  ok
     45%      2,465               0.570                    7.8          9.1  ok
     70%      3,834               0.683                    8.0          6.8  ok
    100%      5,477               0.802                    8.8          5.0  ok
  best comfort at 20% of critical damping, steadiest tyre load at 45%

Too soft and the wheel hops on rough surfaces; too stiff and the body takes every hit (and the tyre
can leave the road over a sharp bump). The setup lives between the two, and finding it took no prototype.
```

## What's in here

| File | Purpose |
|---|---|
| `quartercar.py` | Model, road inputs, simulation and sweep |
| `demo.py` | Damping sweep over both roads |
| `tests/` | Physics sanity checks and the trade-off |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Two masses | Full multibody models in MSC Adams Car or Simulink/Simscape |
| Linear damper | Measured, velocity-dependent damper curves |
| Synthetic road | Measured road profiles and 4-post rig data |
