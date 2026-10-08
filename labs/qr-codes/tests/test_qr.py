import unittest
from qr import make, decode, modules, survives

TEXT = "https://github.com/atonyhonesto"


class QrTests(unittest.TestCase):
    def test_round_trip_every_level(self):
        for level in "LMQH":
            self.assertEqual(decode(make(TEXT, level)), TEXT)

    def test_higher_correction_needs_more_modules(self):
        sizes = [modules(TEXT, lvl) for lvl in "LMQH"]
        self.assertEqual(sizes, sorted(sizes))
        self.assertLess(sizes[0], sizes[-1])

    def test_h_survives_damage_that_breaks_l(self):
        self.assertGreater(survives(TEXT, "H", 0.10), survives(TEXT, "L", 0.10))


if __name__ == "__main__":
    unittest.main()
