import unittest
from graph import BASE, FakeGraph, delta, get_with_retry, read_all


class GraphTests(unittest.TestCase):
    def test_unfiltered_query_hits_threshold(self):
        with self.assertRaises(RuntimeError):
            get_with_retry(FakeGraph(throttle_every=0), BASE, sleep=lambda s: None)

    def test_paging_returns_every_item_once(self):
        g = FakeGraph(n_items=12_000, throttle_every=3)
        rows = read_all(g, "Active")
        ids = [r["id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), sum(1 for i in range(1, 12_001) if i % 5))

    def test_retry_after_is_honoured(self):
        waits = []
        read_all(FakeGraph(n_items=6000, throttle_every=2), "Active", sleep=waits.append)
        self.assertTrue(waits and all(w == 2.0 for w in waits))

    def test_delta_returns_only_changes(self):
        g = FakeGraph(n_items=6000, throttle_every=0)
        _, link = delta(g, None)
        g.update([1, 2])
        changed, _ = delta(g, link)
        self.assertEqual(sorted(r["id"] for r in changed), ["1", "2"])


if __name__ == "__main__":
    unittest.main()
