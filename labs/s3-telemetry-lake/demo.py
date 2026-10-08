import random
import tempfile
from pathlib import Path

from lake import Key, LocalBucket, sync_team_bucket

rng = random.Random(3)
with tempfile.TemporaryDirectory() as tmp:
    official = LocalBucket(Path(tmp) / "official")
    for car in ("5", "11", "24", "48"):
        for lap in range(1, 6):
            k = Key("cup", 2026, "indianapolis", "race", car, lap)
            official.put_object(k.path(), {"lap_time_s": round(49 + rng.random(), 3)})

    prefix = "series=cup/season=2026/event=indianapolis/session=race/car=24/"
    print(f"Objects in lake: {len(official.list_objects())}")
    print(f"Prefix query for car 24: {len(official.list_objects(prefix))} objects")
    team = LocalBucket(Path(tmp) / "team-a")
    n = sync_team_bucket(official, team, cars={"5", "24", "48"})
    print(f"Synced {n} objects to the team bucket; cars present:",
          sorted({k.split('car=')[1].split('/')[0] for k in team.list_objects()}))
