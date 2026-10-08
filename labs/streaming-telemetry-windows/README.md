<sub>[← all labs](../../README.md)</sub>

# Event-time windows over a late, out-of-order telemetry stream

> Radio links reorder packets. Windowing by arrival time gives the wrong answer; windowing by event time needs a watermark.

`Python` · `stdlib`

**Companion to:**
- [Motorsports - Streaming Telemetry & Real-Time Performance](https://www.linkedin.com/pulse/motorsports-streaming-telemetry-real-time-tony-honesto-rfexc/)

## What it shows

- One-second tumbling windows keyed by car and event time.
- A watermark (latest event time minus allowed lateness) decides when a window is final.
- Events older than the watermark are routed to a late-events list instead of silently corrupting closed windows.

## Run it

```bash
bash labs/streaming-telemetry-windows/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
10 one-second windows emitted, 47 events arrived after their window closed
  car 24  t=0s  n=16  vmax=199.0  rpm=9219
  car  5  t=0s  n=14  vmax=196.0  rpm=9287
  car 24  t=1s  n=13  vmax=199.6  rpm=9224
  car  5  t=1s  n=17  vmax=200.0  rpm=9196
```

## What's in here

| File | Purpose |
|---|---|
| `windows.py` | Tumbling window operator with watermark and late-event handling, plus a jittered stream generator |
| `demo.py` | Feeds 5 seconds of 20 Hz telemetry for two cars |
| `tests/` | Out-of-order, lateness and per-car tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Python operator | Apache Flink, Kafka Streams or Spark Structured Streaming |
| Late list | Side output to a dead-letter topic, or allowed lateness with window updates |
| Random arrival jitter | Real RF loss and retransmission at the track |
