from pitwindow import best_pit_lap, fit_degradation, simulate_stints

df = simulate_stints()
model = fit_degradation(df)
print(f"Trained on {len(df)} practice laps from {df.stint.nunique()} stints")
for temp in (28, 42):
    lap, total, times = best_pit_lap(model, race_laps=50, track_temp=temp, window=(15, 35))
    worst = max(times.values())
    print(f"Track {temp}°C: pit on lap {lap}  race time {total/60:.2f} min  "
          f"({worst - total:.1f} s faster than the worst lap in the window)")
