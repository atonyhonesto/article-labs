"""Right-sized boxes vs. a fixed carton catalog.

On-demand packaging machines cut a box to fit each order. The savings come from four places:
  * less corrugate (board area of the box)
  * less void fill (empty space inside)
  * lower dimensional weight, which carriers bill when it exceeds actual weight
  * more parcels per trailer (smaller cube)

Units: inches and pounds, as US carriers bill them.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import permutations

import random

CATALOG = [(8, 6, 4), (10, 8, 6), (12, 10, 8), (14, 12, 10), (18, 14, 12), (20, 16, 14), (24, 18, 18)]
DIM_DIVISOR = 139          # cubic inches per billable pound (common US commercial divisor)
PADDING = 0.5              # inches of clearance on each side for protection
MIN_SIDE = 3.0             # machine limit


@dataclass(frozen=True)
class Item:
    l: float
    w: float
    h: float
    weight: float


def pack_dims(items: list[Item]) -> tuple[float, float, float]:
    """Simple stacking heuristic: lay items flat (largest faces down), stack them, take the bounding box."""
    flat = [sorted((i.l, i.w, i.h), reverse=True) for i in items]
    length = max(f[0] for f in flat)
    width = max(f[1] for f in flat)
    height = sum(f[2] for f in flat)
    return length, width, height


def fits(inner: tuple[float, float, float], box: tuple[float, float, float]) -> bool:
    return any(all(a <= b for a, b in zip(inner, p)) for p in permutations(box))


def catalog_box(inner):
    padded = tuple(d + 2 * PADDING for d in inner)
    options = [b for b in CATALOG if fits(padded, b)]
    return min(options, key=lambda b: b[0] * b[1] * b[2]) if options else None


def custom_box(inner):
    return tuple(max(MIN_SIDE, math.ceil(d + 2 * PADDING)) for d in inner)


def board_area(box) -> float:
    """Regular slotted carton: 2(LW + LH + WH) plus the flap overlap (one extra L*W)."""
    l, w, h = box
    return 2 * (l * w + l * h + w * h) + l * w


def billable(box, weight: float) -> int:
    l, w, h = box
    return math.ceil(max(weight, l * w * h / DIM_DIVISOR))


def compare(order: list[Item]) -> dict:
    inner = pack_dims(order)
    weight = sum(i.weight for i in order)
    item_vol = sum(i.l * i.w * i.h for i in order)
    out = {}
    for name, box in (("catalog", catalog_box(inner)), ("custom", custom_box(inner))):
        if box is None:
            out[name] = None
            continue
        vol = box[0] * box[1] * box[2]
        out[name] = {"box": box, "volume": vol, "board": board_area(box), "void": vol - item_vol,
                     "billable_lb": billable(box, weight)}
    return out


def orders(n=500, seed=7) -> list[list[Item]]:
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        out.append([Item(round(rng.uniform(3, 14), 1), round(rng.uniform(2, 10), 1), round(rng.uniform(0.5, 5), 1),
                         round(rng.uniform(0.2, 4), 1)) for _ in range(rng.choice([1, 1, 1, 2, 2, 3]))])
    return out


def summarise(all_orders) -> dict:
    tot = {k: {"board": 0.0, "void": 0.0, "billable_lb": 0, "volume": 0.0} for k in ("catalog", "custom")}
    oversize = 0
    for order in all_orders:
        r = compare(order)
        if r["catalog"] is None:
            oversize += 1
            continue
        for k in tot:
            for m in tot[k]:
                tot[k][m] += r[k][m]
    tot["oversize"] = oversize
    return tot
