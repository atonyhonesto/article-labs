import json
import unittest

from app import SLACK_SECRET, WEBEX_SECRET, create_app, slack_signature, webex_signature

NOW = 1_800_000_000


class WebhookTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(reply_fn=lambda t: "ok", now=lambda: NOW)
        self.c = self.app.test_client()

    def slack(self, body, ts=NOW, secret=SLACK_SECRET):
        raw = json.dumps(body).encode()
        return self.c.post("/slack/events", data=raw, headers={
            "X-Slack-Request-Timestamp": str(ts), "X-Slack-Signature": slack_signature(secret, str(ts), raw)})

    def test_handshake(self):
        self.assertEqual(self.slack({"type": "url_verification", "challenge": "x"}).get_json(), {"challenge": "x"})

    def test_rejects_bad_signature_and_stale_requests(self):
        ev = {"event_id": "a", "event": {"type": "app_mention", "channel": "C", "text": "hi"}}
        self.assertEqual(self.slack(ev, secret=b"nope").status_code, 401)
        self.assertEqual(self.slack(ev, ts=NOW - 301).status_code, 401)
        self.assertEqual(self.app.config["OUTBOX"], [])

    def test_retries_answered_once(self):
        ev = {"event_id": "b", "event": {"type": "app_mention", "channel": "C", "text": "hi"}}
        self.slack(ev); self.slack(ev)
        self.assertEqual(len(self.app.config["OUTBOX"]), 1)

    def test_ignores_bot_messages(self):
        self.slack({"event_id": "c", "event": {"type": "app_mention", "channel": "C", "text": "hi", "bot_id": "B1"}})
        self.assertEqual(self.app.config["OUTBOX"], [])

    def test_webex_signature(self):
        raw = json.dumps({"id": "w", "data": {"roomId": "R"}}).encode()
        bad = self.c.post("/webex/webhook", data=raw, headers={"X-Spark-Signature": "00"})
        good = self.c.post("/webex/webhook", data=raw, headers={"X-Spark-Signature": webex_signature(WEBEX_SECRET, raw)})
        self.assertEqual((bad.status_code, good.status_code), (401, 200))


if __name__ == "__main__":
    unittest.main()
