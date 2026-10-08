<sub>[← all labs](../../README.md)</sub>

# AppSync-style pub/sub with filtered subscriptions

> A subscription is a standing query. The server's job is to send each client only what it asked for.

`Python` · `asyncio`

**Companion to:**
- [Pub/Sub | AWS AppSync](https://www.linkedin.com/pulse/pubsub-aws-appsync-tony-honesto-qy7cc/)

## What it shows

- Clients subscribe to a mutation field with argument filters (`car='24'`), the way AppSync `@aws_subscribe` subscriptions do.
- A mutation fans out only to subscriptions whose filters match the payload.
- A subscriber with no filters (a data lake) gets everything; a scoped one (one car's pit wall) gets a slice.
- Unsubscribing stops delivery immediately.

## Run it

```bash
bash labs/pubsub-subscriptions/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
11 mutations published
  pit-wall-24  received  3: [{'car': '24', 'lap': 1, 'time_s': 31.2}, {'car': '24', 'lap': 2, 'time_s': 31.2}] ...
  tv-graphics  received  1: [{'car': '5', 'position': 1}]
  data-lake    received  9: [{'car': '24', 'lap': 1, 'time_s': 31.2}, {'car': '5', 'lap': 1, 'time_s': 31.1}] ...
```

## What's in here

| File | Purpose |
|---|---|
| `pubsub.py` | Subscription matching and fan-out |
| `demo.py` | Race mutations delivered to three kinds of subscriber |
| `tests/` | Filter, fan-out and unsubscribe tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| In-process fan-out | AWS AppSync GraphQL subscriptions over WebSockets |
| Python filters | Subscription arguments and enhanced subscription filters in the schema |
| No auth | Cognito / IAM / API-key auth per subscription |
