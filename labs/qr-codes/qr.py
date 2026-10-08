"""Make QR codes, damage them, and see what still scans.

QR codes carry Reed-Solomon error correction at four levels. Higher levels
survive more damage but need more modules (a bigger, denser code):
  L ~7%   M ~15%   Q ~25%   H ~30% of codewords can be recovered.
"""
from __future__ import annotations

import cv2
import numpy as np

LEVELS = {"L": cv2.QRCodeEncoder_CORRECT_LEVEL_L, "M": cv2.QRCodeEncoder_CORRECT_LEVEL_M,
          "Q": cv2.QRCodeEncoder_CORRECT_LEVEL_Q, "H": cv2.QRCodeEncoder_CORRECT_LEVEL_H}


def make(text: str, level: str = "M", scale: int = 8, border: int = 4) -> np.ndarray:
    params = cv2.QRCodeEncoder_Params()
    params.correction_level = LEVELS[level]
    raw = cv2.QRCodeEncoder.create(params).encode(text)          # 1 pixel per module, no quiet zone
    img = cv2.resize(raw, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
    return cv2.copyMakeBorder(img, border * scale, border * scale, border * scale, border * scale,
                              cv2.BORDER_CONSTANT, value=255)


def modules(text: str, level: str) -> int:
    params = cv2.QRCodeEncoder_Params()
    params.correction_level = LEVELS[level]
    return cv2.QRCodeEncoder.create(params).encode(text).shape[0]


def decode(img: np.ndarray) -> str:
    text, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    return text


def damage(img: np.ndarray, fraction: float, seed: int = 0, scale: int = 8, border: int = 4) -> np.ndarray:
    """Paint a solid smudge covering `fraction` of the code's area, like a sticker or a scuff.

    Damage on real labels is clustered, and QR codewords are laid out in 2x4 blocks,
    so a smudge wipes out a few whole codewords rather than one bit in many.
    The smudge is placed at random but kept off the three finder patterns.
    """
    rng = np.random.default_rng(seed)
    out = img.copy()
    n = img.shape[0] // scale - 2 * border
    side = max(1, round((fraction * n * n) ** 0.5))
    lo, hi = 9, n - 9 - side                     # stay clear of finder patterns and separators
    r = int(rng.integers(lo, max(lo + 1, hi + 1)))
    c = int(rng.integers(lo, max(lo + 1, hi + 1)))
    y, x = (r + border) * scale, (c + border) * scale
    out[y:y + side * scale, x:x + side * scale] = 0 if seed % 2 else 255   # dark or light smudge
    return out


def survives(text: str, level: str, fraction: float, trials: int = 10) -> float:
    img = make(text, level)
    return sum(decode(damage(img, fraction, seed=s)) == text for s in range(trials)) / trials
