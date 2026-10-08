from tracking import analyse, simulate_route

t, x, y = simulate_route()
s = analyse(t, x, y)
print(f"Pings: {t.size} over {t[-1]:.0f} s (with a 2 s dropout)")
print(f"Distance {s.distance_m:.0f} m | top speed {s.top_speed_mps:.1f} m/s "
      f"({s.top_speed_mps * 2.237:.1f} mph) | sprints {s.sprints} | max accel {s.max_accel_mps2:.1f} m/s²")
