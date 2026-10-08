<sub>[← all labs](../../README.md)</sub>

# VAR-style offside line with a pitch homography

> A line straight across the pitch isn't straight across the screen. A homography puts it where it really lies.

`Python` · `OpenCV` · `NumPy`

**Companion to:**
- [VAR Graphics in FIFA](https://www.linkedin.com/pulse/var-graphics-fifa-tony-honesto-yo01c/)

## What it shows

- Estimates the image→pitch homography from eight landmarks with OpenCV and RANSAC (one bad click is tolerated).
- Decides offside in pitch metres, not pixels, and reports the margin.
- Projects the offside line back into the camera view and renders it to `out/offside.png`.

## Run it

```bash
bash labs/var-offside-homography/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
attacker 5 cm beyond : offside=True   measured margin +4 cm
attacker 30 cm onside: offside=False  measured margin -29 cm
attacker 90 cm beyond: offside=True   measured margin +90 cm
Offside line in the image runs from (434,576) to (250,184) px: not vertical, because of perspective
Wrote out/offside.png
```

## What's in here

| File | Purpose |
|---|---|
| `offside.py` | Landmarks, homography estimation, offside decision, line projection and rendering |
| `demo.py` | Three attacker positions with ~1 px landmark noise |
| `tests/` | Round-trip, decision, perspective and RANSAC tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Hand-placed landmarks | Automatic pitch-line detection and camera calibration |
| Single foot point | 3D skeletal tracking from multiple calibrated cameras |
| Static frame | Frame-accurate kick-point detection from ball sensors |
