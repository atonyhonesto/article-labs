"""A Twilio inbound-SMS webhook done properly.

* Validates X-Twilio-Signature: base64(HMAC-SHA1(auth_token, full URL + sorted
  POST params concatenated as key+value)). Without this anyone can POST to you.
* Honours opt-out keywords (STOP, UNSUBSCRIBE, ...) and opt-in (START), as
  carriers require.
* Replies with TwiML, Twilio's XML response format, escaping user text.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
from xml.sax.saxutils import escape

from flask import Flask, Response, abort, request

AUTH_TOKEN = "test-auth-token-not-real"
OPT_OUT = {"STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"}
OPT_IN = {"START", "YES", "UNSTOP"}


def twilio_signature(token: str, url: str, params: dict) -> str:
    payload = url + "".join(k + params[k] for k in sorted(params))
    return base64.b64encode(hmac.new(token.encode(), payload.encode(), hashlib.sha1).digest()).decode()


def twiml(message: str | None) -> Response:
    body = f"<Message>{escape(message)}</Message>" if message else ""
    return Response(f'<?xml version="1.0" encoding="UTF-8"?><Response>{body}</Response>', mimetype="text/xml")


def create_app(public_url: str = "https://example.com/sms") -> Flask:
    app = Flask(__name__)
    opted_out: set[str] = set()
    app.config["OPTED_OUT"] = opted_out

    @app.post("/sms")
    def sms():
        params = request.form.to_dict()
        sig = request.headers.get("X-Twilio-Signature", "")
        if not hmac.compare_digest(twilio_signature(AUTH_TOKEN, public_url, params), sig):
            abort(403)
        sender, text = params.get("From", ""), params.get("Body", "").strip()
        word = text.upper()
        if word in OPT_OUT:
            opted_out.add(sender)
            return twiml(None)            # Twilio sends the carrier-standard confirmation itself
        if word in OPT_IN:
            opted_out.discard(sender)
            return twiml("You're subscribed to race-day alerts again. Reply STOP to opt out.")
        if sender in opted_out:
            return twiml(None)
        if word.startswith("TICKETS"):
            return twiml("Gates open at 9:00. Your mobile ticket is in the app under My Events.")
        return twiml(f"Thanks! We got: \"{text}\". Reply TICKETS for gate info or STOP to opt out.")

    return app
