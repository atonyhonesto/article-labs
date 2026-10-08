from pace import driver_pace, stint_degradation, synthetic_session

laps = synthetic_session()
print("Race pace corrected for fuel and tire age (green-flag laps only):")
print(driver_pace(laps).to_string(float_format=lambda v: f"{v:.3f}"))
deg = stint_degradation(laps)
print(f"\nMedian tire degradation: {deg.deg_s_per_lap.median():.3f} s/lap across {len(deg)} stints")
