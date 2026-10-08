import pandas as pd
from pipeline import CATEGORICAL, NUMERIC, build, cross_validated_auc, prospects

df = prospects()
print(f"{len(df)} prospects, {df.made_roster.mean():.0%} made a roster, "
      f"{df[NUMERIC].isna().any(axis=1).mean():.0%} missing some combine data")
print(f"Cross-validated ROC AUC: {cross_validated_auc(df):.3f}")
model = build().fit(df[NUMERIC + CATEGORICAL], df.made_roster)
new = pd.DataFrame([{"sprint_40yd_s": 4.38, "vertical_in": None, "bench_reps": 18, "games_played": 40,
                     "efficiency": 1.4, "position": "WR", "conference_tier": "G5"},
                    {"sprint_40yd_s": 4.85, "vertical_in": 29, "bench_reps": 24, "games_played": 22,
                     "efficiency": -0.3, "position": "TE", "conference_tier": "FCS"}])
for (_, r), p in zip(new.iterrows(), model.predict_proba(new)[:, 1]):
    print(f"  {r.position} from {r.conference_tier}, 40yd {r.sprint_40yd_s}s -> roster probability {p:.0%}")
