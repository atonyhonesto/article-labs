<sub>[← all labs](../../README.md)</sub>

# Real-time motion insight with OpenCV

> Real-time means the work fits inside the frame time. At 30 fps that's 33 ms.

`Python` · `OpenCV`

**Companion to:**
- [Real-Time Video Processing with OpenCV (Python)](https://www.linkedin.com/pulse/real-time-video-processing-opencv-python-tony-honesto-bmgvc/)
- [Real-Time Video Insight with OpenCV + Python](https://www.linkedin.com/pulse/real-time-video-insight-opencv-python-tony-honesto-yrfic/)

## What it shows

- Background subtraction (MOG2), morphological clean-up and contour detection on each frame.
- Halving resolution before processing (4× fewer pixels) and timing every frame against the budget.
- A warm-up period so the background model learns the scene before detections are trusted.
- Estimating an object's speed from its track across frames.

## Run it

```bash
bash labs/opencv-motion-insight/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Object first detected on frame 30 (it appears on frame 30)
Estimated speed 6.0 px/frame (true 6.0)
Processing p50 0.97 ms, p99 1.50 ms against a 33.3 ms budget (30 fps)
```

## What's in here

| File | Purpose |
|---|---|
| `motion.py` | Synthetic frame source, detector and speed estimate |
| `demo.py` | Runs 120 frames and reports detection, speed and latency |
| `tests/` | Noise rejection, detection and speed tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic frames | `cv2.VideoCapture(0)` or an RTSP camera stream |
| Largest-blob track | Multi-object tracking (SORT/ByteTrack) with re-identification |
| CPU only | GPU or NPU acceleration for heavier models (YOLO etc.) |
