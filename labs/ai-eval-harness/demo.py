from harness import Criteria, candidate_model, decide, evaluate, keyword_baseline

c = Criteria()
base = evaluate("keyword baseline", keyword_baseline)
for name, fn, cost in (("candidate model", candidate_model, 0.0008), ("candidate model, bigger tier", candidate_model, 0.004)):
    cand = evaluate(name, fn, cost)
    ok, why = decide(cand, base, c)
    print(f"{name:29} accuracy {cand.accuracy:.0%} (baseline {base.accuracy:.0%}), missed outages {cand.missed_outages}, "
          f"${cand.cost_per_item_usd}/item -> {'GO' if ok else 'NO-GO: ' + '; '.join(why)}")
