from journey import clickstream, funnel, sessionize

df = clickstream()
s = sessionize(df)
print(f"{len(df):,} events from {df.user_id.nunique():,} users -> {s.session_id.nunique():,} sessions")
f = funnel(df, by="device")
f["sessions"] = f.sessions.map("{:,}".format)
f["from_previous"] = f.from_previous.map("{:.0%}".format)
print(f.to_string(index=False))
