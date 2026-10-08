import tempfile
import unittest
from pathlib import Path

from store import features, size_on_disk, training_set, write


class StoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / "f"
        cls.df = features(30_000)
        write(cls.df, cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_partition_pruning(self):
        _, opened = training_set(self.root, "truck", [2024], ["lap_time_s"])
        self.assertEqual(opened, 1)

    def test_slice_matches_pandas(self):
        got, _ = training_set(self.root, "cup", [2025, 2026], ["lap_time_s"])
        want = self.df[(self.df.series == "cup") & self.df.season.isin([2025, 2026])]
        self.assertEqual(len(got), len(want))
        self.assertEqual(list(got.columns), ["lap_time_s"])

    def test_types_survive(self):
        got, _ = training_set(self.root, "cup", [2026], ["tire_age", "fuel_kg"])
        self.assertEqual((str(got.tire_age.dtype), str(got.fuel_kg.dtype)), ("int16", "float32"))

    def test_smaller_than_csv(self):
        csv = Path(self.tmp.name) / "x.csv"
        self.df.to_csv(csv, index=False)
        self.assertLess(size_on_disk(self.root), size_on_disk(csv))


if __name__ == "__main__":
    unittest.main()
