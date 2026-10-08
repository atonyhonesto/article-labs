import numpy as np

from twin import CellParams, Twin, drive_cycle, monitor

current = drive_cycle()
healthy, aged = CellParams(), CellParams(r0_ohm=0.024, r1_ohm=0.016)   # resistance up ~60% with age
for label, real_params in (("healthy cell", healthy), ("aged cell", aged)):
    twin, real = Twin(healthy), Twin(real_params)
    pred = np.array([twin.step(i, 1.0) for i in current])
    meas = np.array([real.step(i, 1.0) for i in current]) + np.random.default_rng(1).normal(0, 0.003, len(current))
    alert = monitor(meas, pred)
    print(f"{label:12}: SOC {real.soc:.2f}, max temp {max(h[2] for h in real.history):.1f} °C, "
          f"mean |V error| {np.abs(meas - pred).mean() * 1000:.1f} mV -> "
          f"{'ALERT at ' + str(alert) + ' s' if alert else 'tracking the twin'}")
