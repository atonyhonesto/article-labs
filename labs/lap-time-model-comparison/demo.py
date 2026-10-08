from compare import evaluate, make_data

df = make_data()
res = evaluate(df)
print(f"{len(df)} laps, {df.stint.nunique()} stints. Mean absolute error in seconds:")
print(res.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
print(f"\nBest on unseen stints: {res.model[0]}")
