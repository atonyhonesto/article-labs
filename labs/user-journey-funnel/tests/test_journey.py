import unittest
import pandas as pd
from journey import funnel, sessionize


def ev(user, minute, event):
    return {"user_id": user, "ts": pd.Timestamp("2026-01-01") + pd.Timedelta(minutes=minute), "event": event, "device": "d"}


class JourneyTests(unittest.TestCase):
    def test_thirty_minute_gap_splits_sessions(self):
        df = pd.DataFrame([ev(1, 0, "event_page"), ev(1, 10, "seat_map"), ev(1, 50, "event_page")])
        self.assertEqual(sessionize(df).session_id.nunique(), 2)

    def test_funnel_is_ordered(self):
        df = pd.DataFrame([ev(1, 0, "purchase"), ev(1, 1, "event_page"), ev(1, 2, "seat_map")])
        f = funnel(df).set_index("step").sessions
        self.assertEqual((f["seat_map"], f["purchase"]), (1, 0))

    def test_steps_never_increase(self):
        from journey import clickstream
        s = funnel(clickstream(300)).sessions.tolist()
        self.assertEqual(s, sorted(s, reverse=True))


if __name__ == "__main__":
    unittest.main()
