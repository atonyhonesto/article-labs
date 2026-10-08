"""KML into numbers: distance, speed and sector times from a GPS track.

Reads a KML `gx:Track` (paired <when> timestamps and <gx:coord> positions) with
the standard library, measures distance along the track with the haversine
formula, and splits the lap at sector-marker placemarks by nearest track point.
"""
from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from datetime import datetime

NS = {"k": "http://www.opengis.net/kml/2.2", "gx": "http://www.google.com/kml/ext/2.2"}
EARTH_R_M = 6_371_000


def haversine_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * EARTH_R_M * math.asin(math.sqrt(h))


def read_track(path: str) -> tuple[list[datetime], list[tuple[float, float]], dict[str, tuple[float, float]]]:
    root = ET.parse(path).getroot()
    track = root.find(".//gx:Track", NS)
    whens = [datetime.fromisoformat(w.text.replace("Z", "+00:00")) for w in track.findall("k:when", NS)]
    coords = []
    for c in track.findall("gx:coord", NS):
        lon, lat, _ = map(float, c.text.split())
        coords.append((lat, lon))
    markers = {}
    for pm in root.findall(".//k:Placemark", NS):
        pt = pm.find("k:Point/k:coordinates", NS)
        if pt is not None:
            lon, lat, *_ = map(float, pt.text.split(","))
            markers[pm.find("k:name", NS).text] = (lat, lon)
    if len(whens) != len(coords):
        raise ValueError("track has mismatched <when> and <gx:coord> counts")
    return whens, coords, markers


def analyse(whens, coords, markers) -> dict:
    seg = [haversine_m(a, b) for a, b in zip(coords, coords[1:])]
    dt = [(b - a).total_seconds() for a, b in zip(whens, whens[1:])]
    speeds = [d / t for d, t in zip(seg, dt) if t > 0]
    cut_idx = sorted(min(range(len(coords)), key=lambda i: haversine_m(coords[i], m)) for m in markers.values())
    bounds = [0] + cut_idx + [len(coords) - 1]
    sectors = [(whens[b] - whens[a]).total_seconds() for a, b in zip(bounds, bounds[1:])]
    return {"distance_m": sum(seg), "lap_s": (whens[-1] - whens[0]).total_seconds(),
            "top_speed_mps": max(speeds), "sectors_s": sectors}
