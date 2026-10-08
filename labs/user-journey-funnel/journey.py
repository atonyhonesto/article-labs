"""User-journey analytics: sessions, an ordered funnel, and where people drop off.

Written in pandas so it runs anywhere; each step maps one-to-one to PySpark
(Window.partitionBy("user_id").orderBy("ts"), lag, sum over window, groupBy).
The PySpark equivalent is in `journey_spark.py` for reference.

* A session ends after 30 minutes of inactivity.
* The funnel is ORDERED: a purchase only counts if it came after viewing seats,
  which came after visiting the event page, within the same session.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FUNNEL = ["event_page", "seat_map", "checkout", "purchase"]
SESSION_GAP = pd.Timedelta(minutes=30)


def clickstream(users: int = 3000, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    t0 = pd.Timestamp("2026-05-01 18:00")
    stay = {"event_page": 0.62, "seat_map": 0.48, "checkout": 0.71}
    for u in range(users):
        t = t0 + pd.Timedelta(minutes=int(rng.integers(0, 600)))
        for visit in range(int(rng.integers(1, 3))):
            for step in FUNNEL:
                rows.append({"user_id": u, "ts": t, "event": step, "device": "mobile" if u % 3 else "desktop"})
                t += pd.Timedelta(seconds=int(rng.integers(20, 240)))
                p = stay.get(step, 0) * (0.8 if (u % 3 and step == "seat_map") else 1.0)
                if step == "purchase" or rng.random() > p:
                    break
            t += pd.Timedelta(hours=int(rng.integers(1, 30)))
    df = pd.DataFrame(rows)
    noise = df.sample(frac=0.03, random_state=1).assign(event="purchase")      # out-of-order noise
    return pd.concat([df, noise]).sort_values(["user_id", "ts"]).reset_index(drop=True)


def sessionize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["user_id", "ts"]).copy()
    new = df.groupby("user_id").ts.diff().gt(SESSION_GAP) | df.user_id.ne(df.user_id.shift())
    df["session_id"] = new.cumsum()
    return df


def funnel(df: pd.DataFrame, by: str | None = None) -> pd.DataFrame:
    """Sessions reaching each step in order."""
    def reached(g: pd.DataFrame) -> int:
        k = 0
        for e in g.event:
            if k < len(FUNNEL) and e == FUNNEL[k]:
                k += 1
        return k

    s = sessionize(df)
    depth = s.groupby("session_id").apply(reached, include_groups=False).rename("depth").to_frame()
    if by:
        depth[by] = s.groupby("session_id")[by].first()
    groups = depth.groupby(by) if by else [("all", depth)]
    rows = []
    for key, g in groups:
        counts = [(g.depth >= i + 1).sum() for i in range(len(FUNNEL))]
        for i, step in enumerate(FUNNEL):
            rows.append({"segment": key, "step": step, "sessions": int(counts[i]),
                         "from_previous": counts[i] / counts[i - 1] if i else 1.0})
    return pd.DataFrame(rows)
