from qlearn import never_pit, optimal_cost, run_policy, train

q = train()
for wear in (0, 6):
    t, stops = run_policy(q, start_wear=wear)
    print(f"start wear {wear}: learned policy pits on laps {stops}, loses {t:.0f} s to wear and stops "
          f"(optimum {optimal_cost(wear):.0f} s, never pitting {never_pit(wear):.0f} s)")
