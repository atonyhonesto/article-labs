import unittest
from intents import build, parse, slots


class IntentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = build()

    def test_typos_still_classify(self):
        self.assertEqual(parse(self.m, "tabel for 2 tonite").intent, "book_table")

    def test_out_of_scope_hands_off(self):
        self.assertTrue(parse(self.m, "my card was charged twice, refund").handoff)

    def test_slots(self):
        self.assertEqual(slots("table for four at 7:30pm"), {"party_size": 4, "time": "19:30"})
        self.assertEqual(slots("party of 6 at 8"), {"party_size": 6, "time": "20:00"})
        self.assertEqual(slots("checkout like 1pm"), {"time": "13:00"})


if __name__ == "__main__":
    unittest.main()
