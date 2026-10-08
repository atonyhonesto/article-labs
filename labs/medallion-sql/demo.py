from pipeline import connect, run_batch

con = connect()
batch1 = [{"race_id": "R1", "car": c, "lap": l, "lap_time_s": t, "recorded_at": f"2026-05-01T12:{l:02d}:00"}
          for c, base in (("24", 31.2), ("5", 31.0)) for l, t in ((1, base + 0.4), (2, base), (3, base + 0.1))]
batch1 += [{"race_id": "R1", "car": "", "lap": 1, "lap_time_s": 31.5, "recorded_at": "2026-05-01T12:01:00"},
           {"race_id": "R1", "car": "48", "lap": 1, "lap_time_s": 9999, "recorded_at": "2026-05-01T12:01:00"}]
print("after batch 1:", run_batch(con, "b1", batch1))
correction = [{"race_id": "R1", "car": "24", "lap": 2, "lap_time_s": 30.95, "recorded_at": "2026-05-01T13:00:00"}]
print("after a timing correction:", run_batch(con, "b2", correction))
print("after replaying batch 1 (late duplicate):", run_batch(con, "b1-replay", batch1))
for row in con.execute("SELECT car, laps, best_lap_s, avg_lap_s FROM gold_car_summary ORDER BY best_lap_s"):
    print("  gold:", row)
print("  rejects:", con.execute("SELECT DISTINCT reason FROM dq_rejects").fetchall())
