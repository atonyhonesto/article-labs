import unittest
from windows import TumblingWindows


def ev(ts, car="1", speed=100.0):
    return {"car": car, "ts_ms": ts, "speed": speed, "rpm": 1000}


class WindowTests(unittest.TestCase):
    def test_out_of_order_event_lands_in_its_own_window(self):
        w = TumblingWindows(1000, 500)
        w.ingest(ev(1100)); w.ingest(ev(900)); out = w.ingest(ev(2600))
        self.assertEqual([(r.start_ms, r.count) for r in out], [(0, 1), (1000, 1)])

    def test_event_behind_watermark_is_late(self):
        w = TumblingWindows(1000, 500)
        w.ingest(ev(3000))
        w.ingest(ev(100))
        self.assertEqual(len(w.late), 1)

    def test_windows_are_per_car(self):
        w = TumblingWindows(1000, 0)
        w.ingest(ev(10, "a")); w.ingest(ev(20, "b"))
        out = w.ingest(ev(1000, "a"))
        self.assertEqual(sorted(r.car for r in out), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
