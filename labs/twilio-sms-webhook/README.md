<sub>[← all labs](../../README.md)</sub>

# A secure Twilio SMS webhook

> Anyone can POST to your webhook. Only Twilio can sign the request.

`Python` · `Flask`

**Companion to:**
- [Twilio for Customer Engagement](https://www.linkedin.com/pulse/twilio-customer-engagement-tony-honesto-hevsc/)

## What it shows

- Verifying `X-Twilio-Signature` (HMAC-SHA1 over the URL and sorted parameters) and rejecting forgeries with 403.
- STOP / START opt-out handling: no replies to opted-out numbers.
- Keyword routing and replies in TwiML, with user text XML-escaped.

## Run it

```bash
bash labs/twilio-sms-webhook/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
'tickets?'             -> 200 <?xml version="1.0" encoding="UTF-8"?><Response><Message>Gates open at 9:00. Your mobile ticket is in the app under My Events.</Message></Response>
'<script>hi</script>'  -> 200 <?xml version="1.0" encoding="UTF-8"?><Response><Message>Thanks! We got: "&lt;script&gt;hi&lt;/script&gt;". Reply TICKETS for gate info or STOP to opt out.</Message></Response>
'STOP'                 -> 200 <?xml version="1.0" encoding="UTF-8"?><Response></Response>
'tickets?'             -> 200 <?xml version="1.0" encoding="UTF-8"?><Response></Response>
'START'                -> 200 <?xml version="1.0" encoding="UTF-8"?><Response><Message>You're subscribed to race-day alerts again. Reply STOP to opt out.</Message></Response>
forged request         -> 403
```

## What's in here

| File | Purpose |
|---|---|
| `app.py` | Flask webhook, signature check and TwiML replies |
| `demo.py` | Signed and forged requests through the Flask test client |
| `tests/` | Signature, opt-out and escaping tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Hand-rolled signature | `twilio.request_validator.RequestValidator` |
| In-memory opt-out set | A database, plus Twilio Advanced Opt-Out |
| Flask test client | A public HTTPS endpoint configured on the Twilio number |
