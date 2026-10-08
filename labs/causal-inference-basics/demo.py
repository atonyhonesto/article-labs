from causal import TRUE_EFFECT, ipw, naive, regression_adjusted, simulate

b, a, y = simulate()
print(f"True effect of the aero package:   {TRUE_EFFECT:+.3f} s/lap")
print(f"Naive difference in means:          {naive(a, y):+.3f} s/lap  <- budget confounds it")
print(f"Regression adjustment for budget:   {regression_adjusted(b, a, y):+.3f} s/lap")
print(f"Inverse propensity weighting:       {ipw(b, a, y):+.3f} s/lap")
