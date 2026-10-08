<sub>[← all labs](../../README.md)</sub>

# An evaluation harness for go/no-go decisions

> AI projects stall when nobody agreed on 'good enough'. Write it down first, then measure.

`Python` · `stdlib`

**Companion to:**
- [Why Most AI Projects Don't Deliver](https://www.linkedin.com/pulse/why-most-ai-projects-dont-deliver-tony-honesto-yuhac/)

## What it shows

- A frozen, labelled evaluation set.
- A simple baseline the AI has to beat.
- Acceptance criteria agreed up front: accuracy, cost per item, p95 latency, and zero tolerance for the costly error (a missed outage).
- A readable GO / NO-GO with the reasons.

## Run it

```bash
bash labs/ai-eval-harness/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
candidate model               accuracy 94% (baseline 88%), missed outages 0, $0.0008/item -> GO
candidate model, bigger tier  accuracy 94% (baseline 88%), missed outages 0, $0.004/item -> NO-GO: cost $0.0040/item > $0.002
```

## What's in here

| File | Purpose |
|---|---|
| `harness.py` | Eval set, criteria, evaluation, decision, baseline and candidate |
| `demo.py` | Judges the candidate at two price points |
| `tests/` | Baseline, launch and blocking-error tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| 16 examples | Hundreds to thousands, refreshed from production |
| Keyword stand-ins | The prompt, fine-tune or vendor model under evaluation |
| One run | Run on every change, tracked over time |
