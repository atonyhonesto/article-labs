import os

import numpy as np

from offside import LANDMARKS_M, camera_homography, estimate_homography, offside_decision, offside_line_px, project, render

rng = np.random.default_rng(0)
truth = camera_homography()
clicks = project(truth, LANDMARKS_M) + rng.normal(0, 1.0, (len(LANDMARKS_M), 2))   # ~1 px click error
H = estimate_homography(LANDMARKS_M, clicks)

defender = project(truth, np.array([[11.30, 40.0]]))[0]
for label, att_m in (("5 cm beyond", [11.25, 20.0]), ("30 cm onside", [11.60, 52.0]), ("90 cm beyond", [10.40, 30.0])):
    attacker = project(truth, np.array([att_m]))[0]
    off, margin = offside_decision(H, attacker, defender)
    print(f"attacker {label:12}: offside={str(off):5}  measured margin {margin * 100:+.0f} cm")
a, b = offside_line_px(H, defender)
print(f"Offside line in the image runs from ({a[0]:.0f},{a[1]:.0f}) to ({b[0]:.0f},{b[1]:.0f}) px: not vertical, because of perspective")
os.makedirs("out", exist_ok=True)
render("out/offside.png", H, project(truth, np.array([[10.40, 30.0]]))[0], defender)
print("Wrote out/offside.png")
