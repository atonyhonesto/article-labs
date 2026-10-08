import unittest
from datetime import datetime, timedelta
from sla import Ticket, counted_time, priority


class SlaTests(unittest.TestCase):
    def test_matrix(self):
        self.assertEqual((priority(1, 1), priority(2, 2), priority(3, 3)), ("P1", "P3", "P5"))

    def test_business_hours_skip_nights_and_weekends(self):
        fri_5pm, mon_9am = datetime(2026, 10, 2, 17), datetime(2026, 10, 5, 9)
        self.assertEqual(counted_time(fri_5pm, mon_9am, False), timedelta(hours=2))

    def test_p1_runs_around_the_clock(self):
        t = Ticket(datetime(2026, 10, 3, 1, 0), 1, 1)       # Saturday 1 am
        self.assertEqual(t.status(datetime(2026, 10, 3, 5, 0))[0], "BREACHED")

    def test_awaiting_customer_pauses_the_clock(self):
        start = datetime(2026, 10, 5, 9)
        t = Ticket(start, 2, 2, [(start + timedelta(hours=1), "awaiting customer"), (start + timedelta(hours=5), "in progress")])
        self.assertEqual(t.elapsed(start + timedelta(hours=6)), timedelta(hours=2))


if __name__ == "__main__":
    unittest.main()
