<sub>[← all labs](../../README.md)</sub>

# Front anti-dive from suspension geometry

> Inclined wishbones can react part of the braking load through the links instead of the springs. Here's how much.

`Python` · `NumPy`

**Companion to:**
- [Anti-Dive & Downwash Geometry in F1](https://www.linkedin.com/pulse/anti-dive-downwash-geometry-f1-tony-honesto-b5xlc/)
- [Helmut Schmidt University - Vehicle Dynamics Certificate](https://www.linkedin.com/pulse/helmut-schmidt-university-vehicle-dynamics-tony-honesto-lanoc/)

## What it shows

- Finds the side-view instant centre from upper and lower wishbone pickups.
- Computes anti-dive percentage from the IC, wheelbase, CG height and front brake share.
- Estimates the resulting nose-down pitch under 5 g braking for three geometries.

## Run it

```bash
bash labs/anti-dive-geometry/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
parallel wishbones : anti-dive   0.0%  nose-down pitch at 5 g braking 0.14°
mild anti-dive     : anti-dive  24.9%  nose-down pitch at 5 g braking 0.10°
strong anti-dive   : anti-dive  74.6%  nose-down pitch at 5 g braking 0.04°
```

## What's in here

| File | Purpose |
|---|---|
| `antidive.py` | Line intersection, anti-dive formula and pitch estimate |
| `demo.py` | Compares parallel, mild and strong anti-dive setups |
| `tests/` | Zero, 100% and sign-convention cases |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| 2D side view | 3D kinematics in a suspension tool (Lotus SHARK, OptimumKinematics, Adams) |
| Single spring rate | Heave springs, inerters and tire vertical stiffness |
| Static geometry | Geometry that moves through bump and roll travel |
