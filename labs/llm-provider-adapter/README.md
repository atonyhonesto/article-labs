<sub>[← all labs](../../README.md)</sub>

# One interface over Bedrock, Gemini and OpenAI

> Providers differ in request shape. Retries, fallback and cost tracking shouldn't be written three times.

`Python` · `stdlib`

**Companion to:**
- [Amazon Bedrock](https://www.linkedin.com/pulse/amazon-bedrock-tony-honesto-gxmpc/)
- [LLM: Gemini](https://www.linkedin.com/pulse/llm-gemini-tony-honesto-nytwc/)
- [ChatGPT + Python](https://www.linkedin.com/pulse/chatgpt-python-tony-honesto-bjsac/)

## What it shows

- Provider classes that only build their own request body and parse their own response (Bedrock Converse, Gemini `generateContent`, Chat Completions).
- Retries with exponential backoff on 429 and 5xx; client errors skip straight to the next provider.
- Fallback across providers, with an attempt log.
- Token and cost accounting per call and in total.

## Run it

```bash
bash labs/llm-provider-adapter/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
healthy:         {'text': 'Bedrock says: box this lap.', 'provider': 'bedrock', 'input_tokens': 120, 'output_tokens': 18, 'cost_usd': 0.00063}
bedrock throttled, gemini blips then answers: gemini - Gemini says: stay out.
attempt log:     [('bedrock', 0, 429), ('bedrock', 1, 429), ('bedrock', 2, 429), ('gemini', 0, 503), ('gemini', 1, 200)]
spend so far:    $0.000208
```

## What's in here

| File | Purpose |
|---|---|
| `adapter.py` | Providers and the router |
| `fake_transport.py` | Fake HTTP returning each provider's real response format |
| `demo.py` | A healthy call, then throttling with fallback |
| `tests/` | Request shapes, backoff, fallback, cost and total-failure tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Fake transport | Signed HTTPS calls (SigV4 for Bedrock, API keys or OAuth for the others) |
| Placeholder prices | Current published per-token prices |
| Sequential fallback | Routing by cost, latency and capability, plus circuit breakers |
