<sub>[← all labs](../../README.md)</sub>

# Kafka consumer groups, offsets and rebalancing

> Kafka promises order per partition and at-least-once delivery. The rest is up to your consumer.

`Python` · `stdlib`

**Companion to:**
- [Apache Kafka | Real-Time Event Streaming](https://www.linkedin.com/pulse/apache-kafka-real-time-event-streaming-tony-honesto-odsrc/)

## What it shows

- Keyed records land on one partition, so a car's laps stay ordered.
- A consumer group splits partitions between members.
- A consumer crashes before committing; after the rebalance its uncommitted records are redelivered.
- An idempotent handler (dedupe on partition + offset) applies every lap exactly once downstream, and lag drains to zero.

## Run it

```bash
bash labs/kafka-consumer-groups/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Assignment: {'analytics-1': [0, 3], 'analytics-2': [1, 4], 'analytics-3': [2, 5]}
analytics-1 processed 15 records, committed 7, then crashed
After rebalance: {'analytics-2': [0, 2, 4], 'analytics-3': [1, 3, 5]} (rebalances: 4)
8 records redelivered to the new owners -> at-least-once; handlers must be idempotent
Laps applied downstream: 25 of 25, 8 duplicates skipped; consumer lag now 0
```

## What's in here

| File | Purpose |
|---|---|
| `kafka_sim.py` | Partitioned topic, consumer group, commits, rebalance and lag |
| `demo.py` | Three consumers, one crash, idempotent apply |
| `tests/` | Ordering, rebalance and redelivery tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| In-memory log | A Kafka / Confluent / MSK / Event Hubs cluster |
| Simple range-style assignment | Cooperative-sticky assignor |
| Dedup set | Idempotent writes or transactional exactly-once processing |
