import unittest
from pathlib import Path

from kml import analyse, haversine_m, read_track

KML = str(Path(__file__).resolve().parent.parent / "lap.kml")


class KmlTests(unittest.TestCase):
    def test_haversine_one_degree_of_latitude(self):
        self.assertAlmostEqual(haversine_m((0, 0), (1, 0)), 111_195, delta=5)

    def test_track_parses_and_closes_the_loop(self):
        w, c, m = read_track(KML)
        self.assertEqual(len(w), len(c))
        self.assertLess(haversine_m(c[0], c[-1]), 1.0)

    def test_sectors_sum_to_the_lap(self):
        r = analyse(*read_track(KML))
        self.assertEqual(len(r["sectors_s"]), 3)
        self.assertAlmostEqual(sum(r["sectors_s"]), r["lap_s"], places=6)


if __name__ == "__main__":
    unittest.main()
