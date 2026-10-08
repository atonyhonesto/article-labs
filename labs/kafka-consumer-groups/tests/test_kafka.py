import unittest
from kafka_sim import ConsumerGroup, Topic


class KafkaTests(unittest.TestCase):
    def setUp(self):
        self.t = Topic("t", 4)
        for i in range(10):
            for k in ("a", "b", "c"):
                self.t.produce(k, {"k": k, "i": i})

    def test_per_key_order(self):
        for part in self.t.log:
            for k in ("a", "b", "c"):
                seq = [v["i"] for key, v in part if key == k]
                self.assertEqual(seq, sorted(seq))

    def test_each_partition_has_one_owner(self):
        g = ConsumerGroup(self.t)
        for m in ("x", "y", "z"):
            g.join(m)
        owned = [p for ps in g.assignment.values() for p in ps]
        self.assertEqual(sorted(owned), [0, 1, 2, 3])

    def test_uncommitted_work_is_redelivered_after_failure(self):
        g = ConsumerGroup(self.t)
        g.join("x"); g.join("y")
        got = g.poll("x")
        g.leave("x")
        again = g.poll("y")
        self.assertTrue({(p, o) for p, o, _, _ in got} <= {(p, o) for p, o, _, _ in again})

    def test_commit_reduces_lag(self):
        g = ConsumerGroup(self.t)
        g.join("x")
        before = g.lag()
        g.commit(g.poll("x", 5))
        self.assertLess(g.lag(), before)


if __name__ == "__main__":
    unittest.main()
