from burnbar import BurnBar

bar = BurnBar(fuel_start=110.0, race_laps=58)
usage = [1.95] * 12 + [1.25] * 3 + [1.92] * 15 + [1.80] * 28
caution = set(range(13, 16))
for lap, used in enumerate(usage, start=1):
    r = bar.update(lap, used, under_caution=lap in caution)
    if lap in (5, 12, 15, 30, 45, 55):
        print(f"lap {lap:2}  avg {r.rolling_avg:.2f} kg vs target {r.target_per_lap:.2f}  "
              f"[{r.bar()}] {r.delta_pct:+5.1f}%  {r.status}")
print(f"Finished with {bar.fuel_left:.1f} kg to spare")
