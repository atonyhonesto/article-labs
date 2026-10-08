"""Real-time motion insight with OpenCV: background subtraction -> contours -> tracked objects.

Frames are synthesised (a moving car-sized blob over a noisy static scene) so the
lab runs anywhere; swap `synthetic_frames()` for `cv2.VideoCapture(0)` or an RTSP
URL and the pipeline is unchanged. Each frame is timed against a budget: at
30 fps a frame has 33 ms, and processing has to fit inside it.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

import cv2
import numpy as np


def synthetic_frames(n: int = 120, w: int = 640, h: int = 360, seed: int = 0):
    """A static scene with sensor noise and one object crossing left to right from frame 30."""
    rng = np.random.default_rng(seed)
    scene = cv2.GaussianBlur(rng.integers(40, 90, (h, w), dtype=np.uint8), (0, 0), 6)
    scene = cv2.cvtColor(scene, cv2.COLOR_GRAY2BGR)
    for i in range(n):
        frame = scene.copy()
        frame = cv2.add(frame, rng.integers(0, 6, frame.shape, dtype=np.uint8))
        if i >= 30:
            x = 20 + (i - 30) * 6
            cv2.rectangle(frame, (x, 160), (x + 60, 200), (200, 200, 230), -1)
        yield frame


@dataclass
class Detection:
    frame: int
    centre: tuple[int, int]
    area: int


@dataclass
class MotionDetector:
    min_area: int = 400
    warmup_frames: int = 10       # let the background model learn the scene before trusting it
    budget_ms: float = 33.3
    subtractor: object = field(default_factory=lambda: cv2.createBackgroundSubtractorMOG2(
        history=60, varThreshold=25, detectShadows=False))
    timings_ms: list = field(default_factory=list)

    def process(self, idx: int, frame: np.ndarray) -> list[Detection]:
        t0 = time.perf_counter()
        small = cv2.resize(frame, None, fx=0.5, fy=0.5)          # halve resolution: 4x less work
        mask = self.subtractor.apply(small)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        if idx < self.warmup_frames:
            self.timings_ms.append((time.perf_counter() - t0) * 1000)
            return []
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        dets = []
        for c in contours:
            area = int(cv2.contourArea(c)) * 4                     # back to full-resolution pixels
            if area >= self.min_area:
                x, y, w, h = cv2.boundingRect(c)
                dets.append(Detection(idx, (2 * x + w, 2 * y + h), area))
        self.timings_ms.append((time.perf_counter() - t0) * 1000)
        return dets


def speed_px_per_frame(dets: list[Detection]) -> float:
    """Average horizontal speed of the largest detection across frames."""
    track = [max(g, key=lambda d: d.area) for g in _by_frame(dets)]
    if len(track) < 2:
        return 0.0
    return (track[-1].centre[0] - track[0].centre[0]) / (track[-1].frame - track[0].frame)


def _by_frame(dets):
    frames = {}
    for d in dets:
        frames.setdefault(d.frame, []).append(d)
    return [frames[k] for k in sorted(frames)]
