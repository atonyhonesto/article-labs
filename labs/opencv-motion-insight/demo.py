import numpy as np

from motion import MotionDetector, speed_px_per_frame, synthetic_frames

det = MotionDetector()
found = []
for i, frame in enumerate(synthetic_frames()):
    found += det.process(i, frame)
first = min(d.frame for d in found) if found else None
t = np.array(det.timings_ms[5:])
print(f"Object first detected on frame {first} (it appears on frame 30)")
print(f"Estimated speed {speed_px_per_frame([d for d in found if d.frame > 35]):.1f} px/frame (true 6.0)")
print(f"Processing p50 {np.percentile(t, 50):.2f} ms, p99 {np.percentile(t, 99):.2f} ms "
      f"against a {det.budget_ms:.1f} ms budget (30 fps)")
