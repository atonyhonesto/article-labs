from quartercar import Car, bump, rough_road, sweep

car = Car()
print(f"Quarter car: body mode {car.body_hz:.2f} Hz, critical damping {car.critical_damping:,.0f} N·s/m")
for name, road, t in (("50 mm x 2 m speed bump at 36 km/h", bump(), 3.0), ("rough road at 90 km/h", rough_road(), 6.0)):
    print(f"\n{name}")
    print("  damping  c (N·s/m)  comfort (m/s² RMS)  tyre load var (% RMS)  travel (mm)  contact")
    results = sweep(car, road, t_end=t)
    for z, c, r in results:
        print(f"  {z:>6.0%}  {c:>9,.0f}  {r['comfort_rms_ms2']:>18.3f}  {r['grip_rms_pct']:>21.1f}  "
              f"{r['travel_mm']:>11.1f}  {'LOST' if r['lost_contact'] else 'ok'}")
    best_comfort = min(results, key=lambda x: x[2]["comfort_rms_ms2"])[0]
    best_grip = min(results, key=lambda x: x[2]["grip_rms_pct"])[0]
    print(f"  best comfort at {best_comfort:.0%} of critical damping, steadiest tyre load at {best_grip:.0%}")
print("\nToo soft and the wheel hops on rough surfaces; too stiff and the body takes every hit (and the tyre")
print("can leave the road over a sharp bump). The setup lives between the two, and finding it took no prototype.")
