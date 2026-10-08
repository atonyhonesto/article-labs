<sub>[← all labs](../../README.md)</sub>

# An agent loop with guardrails

> An agent is a loop: decide, call a tool, look at the result, repeat. The guardrails are what make it safe to run.

`Python` · `stdlib`

**Companion to:**
- [Use Case: Agentic Workflow to Build a Stock Analysis & Reporting Agent](https://www.linkedin.com/pulse/use-case-agentic-workflow-build-stock-analysis-agent-tony-honesto-qetxc/)
- [ChatGPT Agents as "Research and Execution Assistants"](https://www.linkedin.com/pulse/chatgpt-agents-research-execution-assistants-tony-honesto-pc5yc/)

## What it shows

- Tools with declared parameters, validated before they run.
- Tool errors returned to the planner instead of crashing the loop.
- A step budget that stops runaway loops.
- An audit trail of every step, so a human can see how the answer was reached.
- A deterministic planner with the same interface an LLM function-calling planner would use.

## Run it

```bash
bash labs/agent-tool-loop/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Report
- RACE: +24.0% over the period, volatility 23.7% annualised, worst drawdown -1.0%
- PITS: -24.0% over the period, volatility 70.7% annualised, worst drawdown -25.5%
- could not analyse: unknown ticker FAKE

Audit trail:
  {"step": 1, "tool": "compute_stats", "args": {"ticker": "RACE"}, "ok": true}
  {"step": 2, "tool": "compute_stats", "args": {"ticker": "PITS"}, "ok": true}
  {"step": 3, "tool": "compute_stats", "args": {"ticker": "FAKE"}, "ok": false, "error": "unknown ticker FAKE"}
  {"step": 4, "final": true}
```

## What's in here

| File | Purpose |
|---|---|
| `agent.py` | Tools, agent loop and scripted planner over offline price data |
| `demo.py` | Builds a two-ticker report and shows a failed tool call |
| `tests/` | Stats, error-handling and step-budget tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Scripted planner | An LLM with function calling choosing tools from their descriptions |
| Bundled prices | A market-data API, with rate limits and caching |
| Printed report | A reviewed report, with a human approving any action that changes something |
