from pathlib import Path

from kml import analyse, read_track

w, c, m = read_track(str(Path(__file__).with_name("lap.kml")))
r = analyse(w, c, m)
print(f"{len(c)} track points, sector markers {list(m)}")
print(f"Lap distance {r['distance_m']:.0f} m ({r['distance_m'] / 1609.344:.2f} mi), lap time {r['lap_s']:.2f} s, "
      f"average {r['distance_m'] / r['lap_s'] * 2.237:.1f} mph, top {r['top_speed_mps'] * 2.237:.1f} mph")
print("Sector times:", " | ".join(f"S{i + 1} {s:.2f} s" for i, s in enumerate(r["sectors_s"])))
