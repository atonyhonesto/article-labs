from strategy import Track, compare

for rate in (0.01, 0.03, 0.06):
    res = compare(Track(caution_rate=rate), n=2000)
    gain = res["fixed"]["mean_s"] - res["opportunistic"]["mean_s"]
    print(f"caution rate {rate:.2f}/lap: opportunistic saves {gain:5.1f} s on average "
          f"(p90 fixed {res['fixed']['p90_s']/60:.1f} min vs opportunistic {res['opportunistic']['p90_s']/60:.1f} min)")
