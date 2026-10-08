import unittest
from antidive import Wishbone, anti_dive_percent, intersect, pitch_change_deg


class AntiDiveTests(unittest.TestCase):
    def test_parallel_links_give_zero(self):
        up = Wishbone((-0.4, 0.4), (0, 0.4)); lo = Wishbone((-0.4, 0.1), (0, 0.1))
        self.assertEqual(anti_dive_percent(up, lo, 3.6, 0.3, 0.6), 0.0)

    def test_hundred_percent_case(self):
        # IC placed on the line from contact patch to the CG-height point above the rear axle
        wb, h, share = 3.0, 0.3, 1.0
        ic = (-1.0, h / wb)                         # tan(theta) = h / wb -> 100%
        up = Wishbone(ic, (0.0, 0.5)); lo = Wishbone(ic, (0.0, 0.1))
        self.assertAlmostEqual(anti_dive_percent(up, lo, wb, h, share), 100.0, places=6)

    def test_converging_rearward_is_positive(self):
        up = Wishbone((-0.45, 0.39), (0.0, 0.42)); lo = Wishbone((-0.45, 0.14), (0.0, 0.14))
        self.assertGreater(anti_dive_percent(up, lo, 3.6, 0.28, 0.58), 0)

    def test_intersect(self):
        self.assertTrue((intersect((0, 0), (1, 1), (0, 1), (1, 0)) == [0.5, 0.5]).all())

    def test_more_anti_dive_less_pitch(self):
        self.assertLess(pitch_change_deg(5, 800, 0.28, 3.6, 350_000, 40),
                        pitch_change_deg(5, 800, 0.28, 3.6, 350_000, 0))


if __name__ == "__main__":
    unittest.main()
