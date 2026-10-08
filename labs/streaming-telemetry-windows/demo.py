from windows import TumblingWindows, jittered_stream

w = TumblingWindows(size_ms=1000, lateness_ms=500)
results = []
for ev in jittered_stream():
    results += w.ingest(ev)
results += w.flush()
print(f"{len(results)} one-second windows emitted, {len(w.late)} events arrived after their window closed")
for r in results[:4]:
    print(f"  car {r.car:>2}  t={r.start_ms/1000:.0f}s  n={r.count:2}  vmax={r.max_speed:.1f}  rpm={r.avg_rpm:.0f}")
