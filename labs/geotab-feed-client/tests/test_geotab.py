import unittest
from geotab import FakeServer, GeotabClient, InvalidUser


class GeotabTests(unittest.TestCase):
    def test_full_sync_reads_every_record_once(self):
        srv = FakeServer(records=2500)
        rows, v = GeotabClient(srv.call, "d", "u", "demo-password").sync_feed("LogRecord", None)
        self.assertEqual(len({r["id"] for r in rows}), 2500)
        self.assertEqual(v, "2500")

    def test_incremental_sync_only_returns_new(self):
        srv = FakeServer(records=100)
        c = GeotabClient(srv.call, "d", "u", "demo-password")
        _, v = c.sync_feed("LogRecord", None)
        srv.add(5)
        new, _ = c.sync_feed("LogRecord", v)
        self.assertEqual(len(new), 5)

    def test_reauthenticates_on_expired_session(self):
        srv = FakeServer(records=10)
        c = GeotabClient(srv.call, "d", "u", "demo-password")
        c.call("GetFeed", typeName="LogRecord", fromVersion=None)
        srv.expire_session()
        c.call("GetFeed", typeName="LogRecord", fromVersion=None)
        self.assertEqual(srv.calls.count("Authenticate"), 2)

    def test_bad_password_surfaces(self):
        with self.assertRaises(InvalidUser):
            GeotabClient(FakeServer().call, "d", "u", "wrong").call("GetFeed", typeName="LogRecord")


if __name__ == "__main__":
    unittest.main()
