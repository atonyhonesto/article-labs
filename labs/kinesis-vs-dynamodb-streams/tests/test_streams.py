import unittest
from streams import DynamoTableWithStream, KinesisStream, changed_fields, shard_for


class StreamTests(unittest.TestCase):
    def test_same_key_same_shard_in_order(self):
        k = KinesisStream(shards=8)
        for i in range(20):
            k.put_record("car-7", {"i": i}, ts=i)
        shard = shard_for("car-7", 8)
        self.assertEqual([r["data"]["i"] for r in k.read("c", shard)], list(range(20)))

    def test_consumers_have_independent_checkpoints(self):
        k = KinesisStream(shards=1)
        for i in range(3):
            k.put_record("x", {"i": i}, ts=0)
        self.assertEqual(len(k.read("a", 0)), 3)
        self.assertEqual(len(k.read("a", 0)), 0)
        self.assertEqual(len(k.read("b", 0)), 3)

    def test_keys_only_view_hides_images(self):
        t = DynamoTableWithStream(view="KEYS_ONLY")
        t.put_item("k", {"a": 1})
        self.assertNotIn("NewImage", t.stream[0])

    def test_changed_fields(self):
        t = DynamoTableWithStream()
        t.put_item("k", {"a": 1, "b": 2}); t.put_item("k", {"a": 1, "b": 3})
        self.assertEqual(changed_fields(t.stream[1]), {"b": (2, 3)})


if __name__ == "__main__":
    unittest.main()
