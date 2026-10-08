"""Draw a true offside line on a broadcast frame using a pitch homography.

A broadcast camera sees the pitch in perspective, so "a straight line across the
pitch" is not horizontal in the image. Four or more known pitch landmarks give a
homography between pitch metres and image pixels; with it, a player's foot
position becomes a distance down the pitch, and the offside line can be drawn in
camera space exactly where it lies on the grass.
"""
from __future__ import annotations

import cv2
import numpy as np

# Pitch landmarks in metres: x along the length (0 = defending goal line), y across (0..68)
LANDMARKS_M = np.array([
    [0.0, 13.84], [16.5, 13.84], [16.5, 54.16], [0.0, 54.16],   # penalty box corners
    [5.5, 24.84], [5.5, 43.16],                                  # six-yard box front corners
    [52.5, 0.0], [52.5, 68.0],                                   # halfway line ends
], dtype=np.float64)


def camera_homography() -> np.ndarray:
    """A plausible broadcast view (pitch metres -> 1280x720 pixels), used to synthesise observations."""
    src = np.float32([[0, 0], [52.5, 0], [52.5, 68], [0, 68]])
    dst = np.float32([[180, 610], [1240, 470], [930, 130], [40, 200]])
    return cv2.getPerspectiveTransform(src, dst)


def project(H: np.ndarray, pts: np.ndarray) -> np.ndarray:
    return cv2.perspectiveTransform(pts.reshape(-1, 1, 2).astype(np.float64), H).reshape(-1, 2)


def estimate_homography(pitch_m: np.ndarray, image_px: np.ndarray) -> np.ndarray:
    """Image -> pitch homography from clicked or detected landmarks (RANSAC tolerates a bad click)."""
    H, _ = cv2.findHomography(image_px, pitch_m, cv2.RANSAC, 3.0)
    return H


def offside_decision(H_img_to_pitch: np.ndarray, attacker_px, second_last_defender_px) -> tuple[bool, float]:
    """True if the attacker is nearer the goal line than the second-last defender. Returns (offside, margin_m)."""
    att, dfd = project(H_img_to_pitch, np.array([attacker_px, second_last_defender_px], dtype=np.float64))
    margin = dfd[0] - att[0]          # positive: attacker is beyond the defender, toward goal
    return bool(margin > 0), float(margin)


def offside_line_px(H_img_to_pitch: np.ndarray, defender_px) -> np.ndarray:
    """The two image endpoints of the line across the pitch through the defender's position."""
    x_def = project(H_img_to_pitch, np.array([defender_px], dtype=np.float64))[0, 0]
    H_pitch_to_img = np.linalg.inv(H_img_to_pitch)
    return project(H_pitch_to_img, np.array([[x_def, 0.0], [x_def, 68.0]]))


def render(path: str, H_img_to_pitch, attacker_px, defender_px) -> None:
    img = np.full((720, 1280, 3), (60, 140, 60), np.uint8)
    H_pitch_to_img = np.linalg.inv(H_img_to_pitch)
    for x in range(0, 53, 5):                             # pitch stripes, to show perspective
        a, b = project(H_pitch_to_img, np.array([[x, 0.0], [x, 68.0]])).astype(int)
        cv2.line(img, tuple(a), tuple(b), (70, 160, 70), 1)
    a, b = offside_line_px(H_img_to_pitch, defender_px).astype(int)
    cv2.line(img, tuple(a), tuple(b), (0, 255, 255), 2)
    cv2.circle(img, tuple(map(int, defender_px)), 7, (255, 80, 80), -1)
    cv2.circle(img, tuple(map(int, attacker_px)), 7, (60, 60, 255), -1)
    cv2.imwrite(path, img)
