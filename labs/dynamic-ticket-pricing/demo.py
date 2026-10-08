from pricing import Section, best_price, demand, fit_elasticity, history, intercept_for

# (name, seats sold at the reference price, reference price, true elasticity, section)
sections = [("Lower bowl", 450, 140, -1.4, Section("Lower bowl", 400, 90, 260, 140)),
            ("Upper deck", 2200, 60, -2.3, Section("Upper deck", 2500, 35, 110, 60))]
for name, sold_ref, p_ref, tb, sec in sections:
    ta = intercept_for(sold_ref, p_ref, tb)
    a, b = fit_elasticity(*history(ta, tb, lo=0.5 * p_ref, hi=1.5 * p_ref))
    price, rev = best_price(sec, a, b)
    now = sec.current * min(demand(a, b, sec.current), sec.seats_left)
    print(f"{name:11}: elasticity {b:.2f} (true {tb})  ${sec.current:.0f} -> ${price:.0f}  "
          f"expected revenue ${now:,.0f} -> ${rev:,.0f}")
