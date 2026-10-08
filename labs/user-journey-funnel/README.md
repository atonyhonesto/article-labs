<sub>[← all labs](../../README.md)</sub>

# User journey analytics: sessions and funnels

> A funnel is only honest if steps happen in order within a session. Otherwise you're counting coincidences.

`Python` · `pandas`

**Companion to:**
- [User Journey Analytics with PySpark](https://www.linkedin.com/pulse/user-journey-analytics-pyspark-tony-honesto-ckqbc/)

## What it shows

- Sessionising clickstream events with a 30-minute inactivity gap.
- An ordered funnel (event page → seat map → checkout → purchase) where a step only counts after the previous one.
- Step-to-step conversion by segment, which shows mobile losing users at checkout.
- `journey_spark.py`: the same logic with PySpark window functions for data that doesn't fit in memory.

## Run it

```bash
bash labs/user-journey-funnel/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
9,522 events from 3,000 users -> 4,504 sessions
segment       step sessions from_previous
desktop event_page    1,504          100%
desktop   seat_map      933           62%
desktop   checkout      446           48%
desktop   purchase      308           69%
 mobile event_page    3,000          100%
 mobile   seat_map    1,897           63%
 mobile   checkout      682           36%
 mobile   purchase      484           71%
```

## What's in here

| File | Purpose |
|---|---|
| `journey.py` | Synthetic clickstream, sessionise and funnel (pandas) |
| `journey_spark.py` | PySpark equivalent (reference) |
| `demo.py` | Funnel by device |
| `tests/` | Session gap and ordering tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic events | Web/app analytics events (Segment, GA4 export, Snowplow) |
| pandas | PySpark on Databricks / EMR via `journey_spark.py` |
| Printed table | Dashboard plus A/B tests on the leakiest step |
