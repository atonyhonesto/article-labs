import asyncio
import unittest
from pubsub import PubSub, drain


class PubSubTests(unittest.TestCase):
    def test_filters(self):
        ps = PubSub()
        s = ps.subscribe("c", "onLap", car="1")
        ps.mutate("onLap", {"car": "2"}); ps.mutate("onLap", {"car": "1"}); ps.mutate("other", {"car": "1"})
        self.assertEqual(asyncio.run(drain(s)), [{"car": "1"}])

    def test_slow_subscriber_drops_oldest_without_blocking_others(self):
        ps = PubSub()
        slow = ps.subscribe("slow", "f")
        for i in range(60):
            ps.mutate("f", {"i": i})
        msgs = asyncio.run(drain(slow))
        self.assertEqual((len(msgs), slow.dropped, msgs[0]["i"]), (50, 10, 10))

    def test_unsubscribe(self):
        ps = PubSub()
        s = ps.subscribe("c", "f")
        ps.unsubscribe(s)
        self.assertEqual(ps.mutate("f", {}), 0)


if __name__ == "__main__":
    unittest.main()
