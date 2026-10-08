<sub>[← all labs](../../README.md)</sub>

# RFID player tracking → broadcast stats

> Tags in the shoulder pads report position ten times a second. Turning that into 'top speed 21 mph' takes more care than it looks.

`Python` · `NumPy`

**Companion to:**
- [Zebra Technologies MotionWorks RFID](https://www.linkedin.com/pulse/zebra-technologies-motionworks-rfid-tony-honesto-pa5mc/)

## What it shows

- Smooths jittery positions per unbroken run of pings, so a dropout never blends two locations.
- Never integrates distance or speed across a gap in the data.
- Counts sprints with hysteresis (enter at 7 m/s, exit below 6 m/s) so noise around the threshold isn't double-counted.

## Run it

```bash
bash labs/rfid-player-tracking/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Pings: 581 over 60 s (with a 2 s dropout)
Distance 212 m | top speed 9.2 m/s (20.6 mph) | sprints 2 | max accel 6.6 m/s²
```

## What's in here

| File | Purpose |
|---|---|
| `tracking.py` | Smoothing, gap handling, speed/acceleration and sprint detection, plus a route simulator |
| `demo.py` | Analyses a 60-second route with two sprints and a 2-second dropout |
| `tests/` | Sprint count, top speed and dropout tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Simulated 10 Hz pings | Ultra-wideband RFID feed (location, tag ID, timestamp) |
| Moving-average smoothing | Kalman filtering with a motion model |
| Single player | Every player and the ball, streamed to graphics and analytics in real time |
