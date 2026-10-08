import json
import time

from app import SLACK_SECRET, WEBEX_SECRET, create_app, slack_signature, webex_signature

app = create_app()
c = app.test_client()


def slack(body: dict, ts: int | None = None, secret: bytes = SLACK_SECRET):
    raw = json.dumps(body).encode()
    ts = str(ts or int(time.time()))
    return c.post("/slack/events", data=raw, headers={"X-Slack-Request-Timestamp": ts,
                                                       "X-Slack-Signature": slack_signature(secret, ts, raw)})


mention = {"event_id": "Ev1", "event": {"type": "app_mention", "channel": "C1", "text": "<@bot> pit window for car 24?"}}
print("Slack handshake       ->", slack({"type": "url_verification", "challenge": "abc"}).get_json())
print("Signed mention        ->", slack(mention).status_code)
print("Slack retry (same id) ->", slack(mention).status_code, "(acknowledged, not re-answered)")
print("Forged signature      ->", slack(mention, secret=b"wrong").status_code)
print("Replayed (10 min old) ->", slack({**mention, "event_id": "Ev2"}, ts=int(time.time()) - 600).status_code)
raw = json.dumps({"id": "wh1", "data": {"roomId": "R9", "_demo_text": "tire temps?"}}).encode()
print("Webex signed message  ->", c.post("/webex/webhook", data=raw,
                                          headers={"X-Spark-Signature": webex_signature(WEBEX_SECRET, raw)}).status_code)
print("Replies queued:", json.dumps(app.config["OUTBOX"], indent=1))
