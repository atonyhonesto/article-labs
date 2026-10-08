"""Slack and Webex webhook receivers for an LLM-backed bot.

The two jobs that matter before any AI runs:
* prove the request really came from Slack/Webex (HMAC signature over the raw body)
* refuse replays (Slack: timestamp older than 5 minutes; both: duplicate event IDs)

The reply itself goes through `reply_fn`, so any LLM (OpenAI, Bedrock, a local
model) can be plugged in. Here it's a deterministic stub so the lab runs offline.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Callable

from flask import Flask, abort, jsonify, request

SLACK_SECRET = b"slack-signing-secret-for-tests"
WEBEX_SECRET = b"webex-webhook-secret-for-tests"
MAX_AGE_S = 300


def slack_signature(secret: bytes, timestamp: str, body: bytes) -> str:
    base = b"v0:" + timestamp.encode() + b":" + body
    return "v0=" + hmac.new(secret, base, hashlib.sha256).hexdigest()


def webex_signature(secret: bytes, body: bytes) -> str:
    return hmac.new(secret, body, hashlib.sha1).hexdigest()


def default_reply(text: str) -> str:
    return f"(stub model) You asked: '{text.strip()}'. Plug an LLM into reply_fn to answer for real."


def create_app(reply_fn: Callable[[str], str] = default_reply, now: Callable[[], float] = time.time) -> Flask:
    app = Flask(__name__)
    seen: set[str] = set()
    outbox: list[dict] = []
    app.config["OUTBOX"] = outbox

    @app.post("/slack/events")
    def slack_events():
        raw = request.get_data()
        ts = request.headers.get("X-Slack-Request-Timestamp", "0")
        if abs(now() - int(ts)) > MAX_AGE_S:
            abort(401, "stale request")
        if not hmac.compare_digest(slack_signature(SLACK_SECRET, ts, raw),
                                   request.headers.get("X-Slack-Signature", "")):
            abort(401, "bad signature")
        body = json.loads(raw)
        if body.get("type") == "url_verification":           # one-time handshake when the app is configured
            return jsonify({"challenge": body["challenge"]})
        event_id = body.get("event_id", "")
        if event_id in seen:                                  # Slack retries if we're slow: acknowledge, do nothing
            return "", 200
        seen.add(event_id)
        ev = body.get("event", {})
        if ev.get("type") == "app_mention" and not ev.get("bot_id"):
            outbox.append({"channel": "slack", "to": ev["channel"], "text": reply_fn(ev.get("text", ""))})
        return "", 200

    @app.post("/webex/webhook")
    def webex_webhook():
        raw = request.get_data()
        if not hmac.compare_digest(webex_signature(WEBEX_SECRET, raw), request.headers.get("X-Spark-Signature", "")):
            abort(401, "bad signature")
        body = json.loads(raw)
        if body.get("id") in seen:
            return "", 200
        seen.add(body.get("id"))
        data = body.get("data", {})
        # A real bot GETs /v1/messages/{data.id} with its token; the text is not in the webhook body.
        text = data.get("_demo_text", "")
        outbox.append({"channel": "webex", "to": data.get("roomId"), "text": reply_fn(text)})
        return "", 200

    return app
