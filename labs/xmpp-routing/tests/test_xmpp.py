import unittest
from xmpp import JID, Network, Server, stanza


class XmppTests(unittest.TestCase):
    def setUp(self):
        self.net = Network()
        self.a = self.net.add(Server("a.example"))
        self.b = self.net.add(Server("b.example"))
        self.alice = JID.parse("Alice@A.example/pc")
        self.bob = JID.parse("bob@b.example/phone")

    def test_jid_parsing(self):
        self.assertEqual(str(self.alice), "alice@a.example/pc")
        self.assertEqual(str(self.alice.bare), "alice@a.example")
        with self.assertRaises(ValueError):
            JID.parse("no-at-sign")

    def test_offline_then_delivered_on_login(self):
        self.a.login(self.alice)
        self.a.send(stanza("message", self.alice, self.bob.bare, "hi"))
        self.assertEqual(len(self.b.offline[self.bob.bare]), 1)
        self.assertEqual(len(self.b.login(self.bob)), 1)
        self.assertNotIn(self.bob.bare, self.b.offline)

    def test_bare_jid_goes_to_highest_priority(self):
        self.b.login(self.bob, priority=1)
        tablet = JID.parse("bob@b.example/tablet")
        self.b.login(tablet, priority=9)
        self.a.login(self.alice)
        self.a.send(stanza("message", self.alice, self.bob.bare, "x"))
        self.assertEqual(len(self.b.inbox[tablet]), 1)
        self.assertEqual(len(self.b.inbox[self.bob]), 0)

    def test_presence_needs_subscription(self):
        self.a.login(self.alice)
        self.b.login(self.bob)
        self.assertEqual(self.a.inbox[self.alice], [])
        self.b.approve(self.bob, self.alice)
        self.b.logout(self.bob)
        self.assertIn('type="unavailable"', self.a.inbox[self.alice][-1])

    def test_unknown_domain(self):
        self.a.login(self.alice)
        with self.assertRaises(LookupError):
            self.a.send(stanza("message", self.alice, JID.parse("x@nowhere.example"), "?"))

    def test_spoofed_from_dropped(self):
        self.b.login(self.bob)
        self.b.receive(stanza("message", JID.parse("eve@b.example"), self.bob, "x"), from_remote="a.example")
        self.assertEqual(self.b.inbox[self.bob], [])


if __name__ == "__main__":
    unittest.main()
