from ers import PowerUnit, simulate_lap, sustainable_deploy_fraction

for label, pu in (("with MGU-H (pre-2026)", PowerUnit(mguk_kw=120, mguh_kw=60)),
                  ("no MGU-H, 350 kW MGU-K (2026)", PowerUnit(mguk_kw=350, mguh_kw=0))):
    frac = sustainable_deploy_fraction(pu)
    deployed, _ = simulate_lap(pu, pu.battery_mj, frac)
    print(f"{label:30}: can deploy {frac:5.1%} of full MGU-K power on every straight, "
          f"{deployed:.2f} MJ per lap without draining the battery")
