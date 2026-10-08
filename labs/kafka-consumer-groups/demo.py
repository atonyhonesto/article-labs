from kafka_sim import ConsumerGroup, Topic

t = Topic("lap-times", partitions=6)
for lap in range(1, 6):
    for car in ("5", "11", "24", "48", "77"):
        t.produce(car, {"car": car, "lap": lap})

g = ConsumerGroup(t)
for m in ("analytics-1", "analytics-2", "analytics-3"):
    g.join(m)
print("Assignment:", g.assignment)
batch = g.poll("analytics-1")
g.commit(batch[: len(batch) // 2])          # crashes after committing only half of what it processed
print(f"analytics-1 processed {len(batch)} records, committed {len(batch) // 2}, then crashed")
g.leave("analytics-1")
print("After rebalance:", g.assignment, f"(rebalances: {g.rebalances})")
done_keys = {(p, o) for p, o, _, _ in batch}
redelivered = [r for m in g.members for r in g.poll(m) if (r[0], r[1]) in done_keys]
print(f"{len(redelivered)} records redelivered to the new owners -> at-least-once; handlers must be idempotent")
applied = {(v["car"], v["lap"]) for _, _, _, v in batch}   # what analytics-1 had already written downstream
skipped = 0
for m in g.members:
    recs = g.poll(m, max_records=100)
    for p, off, k, v in recs:
        if (v["car"], v["lap"]) in applied:       # idempotent write: a lap is applied once however often it arrives
            skipped += 1
        else:
            applied.add((v["car"], v["lap"]))
    g.commit(recs)
print(f"Laps applied downstream: {len(applied)} of {sum(len(p) for p in t.log)}, "
      f"{skipped} duplicates skipped; consumer lag now {g.lag()}")
