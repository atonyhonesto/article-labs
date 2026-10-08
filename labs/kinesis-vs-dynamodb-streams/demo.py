from streams import DynamoTableWithStream, KinesisStream, changed_fields

k = KinesisStream(shards=2)
for i, car in enumerate(["24", "5", "24", "48", "24", "5"]):
    k.put_record(car, {"car": car, "lap": i // 2 + 1}, ts=i)
s24 = [s for s in range(2) if any(r["key"] == "24" for r in k._log[s])][0]
print("Kinesis: car 24 laps in order on shard", s24, "->", [r["data"]["lap"] for r in k.read("strategy-app", s24) if r["key"] == "24"])
print("         a second consumer reads the same records from its own checkpoint:",
      len(k.read("archiver", s24)), "records")
k.expire(now=24 * 3600 + 3)
print("         after 24 h retention, records left:", sum(len(s) for s in k._log))

t = DynamoTableWithStream()
t.put_item("car#24", {"position": 3, "tires": "soft"})
t.put_item("car#24", {"position": 1, "tires": "soft"})
t.delete_item("car#24")
print("DynamoDB stream:", [r["eventName"] for r in t.stream])
print("  MODIFY changed:", changed_fields(t.stream[1]))
