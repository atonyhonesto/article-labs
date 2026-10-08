<sub>[← all labs](../../README.md)</sub>

# Conversational ML: intents, slots and a human handoff

> Most chatbot failures are confident wrong answers. This one knows when to hand over.

`Python` · `scikit-learn`

**Companion to:**
- [Conversational ML](https://www.linkedin.com/pulse/conversational-ml-tony-honesto-rsycc/)
- [The Cosmopolitan's AI Rose SMS Chatbot](https://www.linkedin.com/pulse/cosmopolitans-ai-rose-sms-chatbot-tony-honesto-rxmec/)

## What it shows

- Intent classification from word and character n-grams, so texting typos still classify.
- Simple, explicit slot extraction for party size and time.
- A confidence threshold below which the conversation goes to a human.

## Run it

```bash
bash labs/intent-classifier/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
'hey can u get us a table for 4 at 8:30'                       -> book_table    conf 0.76 slots {'party_size': 4, 'time': '20:30'}
'is the spa open tmrw'                                         -> spa           conf 0.76 slots {}
'late checkout? like 1pm'                                      -> late_checkout conf 0.89 slots {'time': '13:00'}
"what's the wifi password and also my card was charged twice"  -> HUMAN         conf 0.29 slots {}
```

## What's in here

| File | Purpose |
|---|---|
| `intents.py` | Training phrases, model, slot extractors and parser |
| `demo.py` | Four guest messages, one out of scope |
| `tests/` | Typo, handoff and slot tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| A few dozen examples | Thousands of real, labelled conversations |
| Regex slots | A sequence-labelling model or LLM extraction with validation |
| Threshold only | Handoff on low confidence, repeated failure or sensitive topics |
