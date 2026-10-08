<sub>[← all labs](../../README.md)</sub>

# Slack and Webex webhooks for an LLM bot

> Before any AI runs, prove the message is real and that you haven't seen it before.

`Python` · `Flask`

**Companion to:**
- [ChatGPT + Slack](https://www.linkedin.com/pulse/chatgpt-slack-tony-honesto-jcmjc/)
- [ChatGPT + Webex Webhooks](https://www.linkedin.com/pulse/chatgpt-webex-webhooks-tony-honesto-uh5tc/)

## What it shows

- Slack request signing: HMAC-SHA256 over `v0:timestamp:body`, compared in constant time.
- Replay protection: requests older than five minutes are rejected; retried event IDs are acknowledged but not re-answered.
- Slack's `url_verification` handshake and ignoring the bot's own messages.
- Webex webhook signatures (HMAC-SHA1 in `X-Spark-Signature`).
- A pluggable `reply_fn`, so any LLM can write the answer.

## Run it

```bash
bash labs/chat-webhook-bot/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Slack handshake       -> {'challenge': 'abc'}
Signed mention        -> 200
Slack retry (same id) -> 200 (acknowledged, not re-answered)
Forged signature      -> 401
Replayed (10 min old) -> 401
Webex signed message  -> 200
Replies queued: [
 {
  "channel": "slack",
  "to": "C1",
  "text": "(stub model) You asked: '<@bot> pit window for car 24?'. Plug an LLM into reply_fn to answer for real."
 },
 {
  "channel": "webex",
  "to": "R9",
  "text": "(stub model) You asked: 'tire temps?'. Plug an LLM into reply_fn to answer for real."
 }
]
```

## What's in here

| File | Purpose |
|---|---|
| `app.py` | Flask app with both endpoints, signature helpers and an outbox |
| `demo.py` | Handshake, signed, retried, forged and replayed requests |
| `tests/` | Signature, staleness, retry and bot-loop tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Hard-coded secrets | Secrets from a vault or environment |
| In-memory dedupe | Redis/DynamoDB with TTL |
| Outbox list | Slack `chat.postMessage` / Webex `POST /v1/messages`, sent from a queue so the webhook returns fast |
