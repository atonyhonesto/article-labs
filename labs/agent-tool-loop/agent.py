"""An agent loop with guardrails: typed tools, a step budget and an audit trail.

The "planner" decides which tool to call next. In production it's an LLM using
function calling; here it's a deterministic planner with the same interface, so
the loop, the tools and the guardrails are testable offline.

Data is a bundled price series, so nothing here is investment advice: it shows
how an agent gathers facts with tools and writes a report from them.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from typing import Callable

PRICES = {  # fictional tickers, 20 trading days of closes
    "RACE": [100, 101, 103, 102, 104, 107, 106, 108, 111, 110, 112, 115, 114, 116, 118, 117, 120, 122, 121, 124],
    "PITS": [50, 49, 51, 48, 47, 49, 46, 45, 47, 44, 43, 45, 42, 41, 43, 40, 41, 39, 40, 38],
}


@dataclass
class Tool:
    name: str
    description: str
    params: dict
    fn: Callable[..., dict]

    def call(self, args: dict) -> dict:
        missing = [p for p in self.params if p not in args]
        if missing:
            raise ValueError(f"{self.name}: missing {missing}")
        return self.fn(**{k: args[k] for k in self.params})


def get_prices(ticker: str) -> dict:
    if ticker not in PRICES:
        raise ValueError(f"unknown ticker {ticker}")
    return {"ticker": ticker, "closes": PRICES[ticker]}


def compute_stats(ticker: str) -> dict:
    p = get_prices(ticker)["closes"]
    rets = [b / a - 1 for a, b in zip(p, p[1:])]
    mean = sum(rets) / len(rets)
    vol = math.sqrt(sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)) * math.sqrt(252)
    peak, dd = p[0], 0.0
    for x in p:
        peak = max(peak, x)
        dd = min(dd, x / peak - 1)
    return {"ticker": ticker, "return_pct": round((p[-1] / p[0] - 1) * 100, 1),
            "annual_vol_pct": round(vol * 100, 1), "max_drawdown_pct": round(dd * 100, 1)}


TOOLS = {t.name: t for t in [
    Tool("get_prices", "Daily closing prices for a ticker", {"ticker": "string"}, get_prices),
    Tool("compute_stats", "Return, volatility and drawdown for a ticker", {"ticker": "string"}, compute_stats),
]}


@dataclass
class Agent:
    planner: Callable[[str, list], dict]
    max_steps: int = 6
    trail: list = field(default_factory=list)

    def run(self, goal: str) -> str:
        for step in range(1, self.max_steps + 1):
            action = self.planner(goal, self.trail)
            if action["type"] == "final":
                self.trail.append({"step": step, "final": True})
                return action["text"]
            tool = TOOLS.get(action["tool"])
            try:
                if tool is None:
                    raise ValueError(f"no such tool {action['tool']}")
                result = tool.call(action["args"])
                self.trail.append({"step": step, "tool": tool.name, "args": action["args"], "ok": True, "result": result})
            except ValueError as e:                       # errors go back to the planner, not up the stack
                self.trail.append({"step": step, "tool": action["tool"], "args": action["args"], "ok": False, "error": str(e)})
        return "Stopped: step budget exhausted before a final answer."


def scripted_planner(goal: str, trail: list) -> dict:
    """Stand-in for an LLM: compute stats for each ticker in the goal, then write the report."""
    wanted = [w.strip(",.?") for w in goal.split() if w.strip(",.?").isupper() and len(w.strip(",.?")) >= 3]
    done = {t["args"]["ticker"] for t in trail if t.get("tool") == "compute_stats"}
    for ticker in wanted:
        if ticker not in done:
            return {"type": "tool", "tool": "compute_stats", "args": {"ticker": ticker}}
    stats = [t["result"] for t in trail if t.get("ok") and t.get("tool") == "compute_stats"]
    errors = [t["error"] for t in trail if not t.get("ok", True)]
    lines = [f"- {s['ticker']}: {s['return_pct']:+.1f}% over the period, volatility {s['annual_vol_pct']}% "
             f"annualised, worst drawdown {s['max_drawdown_pct']}%" for s in stats]
    lines += [f"- could not analyse: {e}" for e in errors]
    return {"type": "final", "text": "Report\n" + "\n".join(lines)}
