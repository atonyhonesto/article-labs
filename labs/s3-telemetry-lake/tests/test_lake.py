import tempfile
import unittest
from pathlib import Path

from lake import Key, LocalBucket, sync_team_bucket


class LakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.src = LocalBucket(Path(self.tmp.name) / "src")
        for car in ("1", "2"):
            for lap in (1, 2, 10):
                self.src.put_object(Key("cup", 2026, "x", "race", car, lap).path(), {"lap": lap})

    def tearDown(self):
        self.tmp.cleanup()

    def test_keys_sort_by_lap_thanks_to_zero_padding(self):
        laps = [k.rsplit("lap=", 1)[1] for k in self.src.list_objects("series=cup/season=2026/event=x/session=race/car=1/")]
        self.assertEqual(laps, ["001.json", "002.json", "010.json"])

    def test_team_sync_never_leaks_other_cars(self):
        dst = LocalBucket(Path(self.tmp.name) / "dst")
        self.assertEqual(sync_team_bucket(self.src, dst, {"2"}), 3)
        self.assertTrue(all("car=2/" in k for k in dst.list_objects()))

    def test_round_trip(self):
        k = Key("cup", 2026, "x", "race", "1", 2).path()
        self.assertEqual(self.src.get_object(k), {"lap": 2})


if __name__ == "__main__":
    unittest.main()
