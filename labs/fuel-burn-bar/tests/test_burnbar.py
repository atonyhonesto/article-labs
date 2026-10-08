import unittest
from burnbar import BurnBar


class BurnBarTests(unittest.TestCase):
    def test_over_burning_flags_save_fuel(self):
        b = BurnBar(100, 50)
        r = None
        for lap in range(1, 6):
            r = b.update(lap, 2.3)
        self.assertEqual(r.status, "SAVE FUEL")

    def test_caution_laps_do_not_flatter_average(self):
        b = BurnBar(100, 50)
        for lap in range(1, 4):
            b.update(lap, 2.0)
        r = b.update(4, 1.0, under_caution=True)
        self.assertAlmostEqual(r.rolling_avg, 2.0)

    def test_bar_centre_when_on_target(self):
        b = BurnBar(100, 50)
        r = b.update(1, 2.0)
        self.assertEqual(r.bar(5), "--#--".replace("#", "|"))


if __name__ == "__main__":
    unittest.main()
