"""Why most AI projects don't deliver: nobody defined "good enough" before building.

This harness makes the decision explicit:
1. a frozen, labelled evaluation set
2. a simple baseline the AI must beat
3. acceptance criteria agreed up front (accuracy, cost per item, latency, and a
   hard cap on the worst kind of error)
4. a go/no-go report anyone can read

The "AI" here is any callable, so a prompt, a fine-tuned model or a vendor API
can be dropped in and judged on the same terms.
"""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from typing import Callable

# Ticket triage: route support messages to a queue. Misrouting an outage is the costly error.
EVAL_SET = [
    ("site is down for all users", "outage"), ("cannot log in since this morning", "outage"),
    ("checkout page returns 500", "outage"), ("api timing out across regions", "outage"),
    ("refund my last order", "billing"), ("charged twice this month", "billing"),
    ("update my card", "billing"), ("invoice shows wrong tax", "billing"),
    ("how do i export a report", "how_to"), ("where is dark mode", "how_to"),
    ("can i add a teammate", "how_to"), ("change my username", "how_to"),
    ("payments failing for everyone", "outage"), ("dashboard blank for whole team", "outage"),
    ("cancel my subscription", "billing"), ("how to reset password", "how_to"),
]


@dataclass(frozen=True)
class Criteria:
    min_accuracy: float = 0.85
    max_missed_outages: int = 0          # the error that actually hurts
    max_cost_per_item_usd: float = 0.002
    max_p95_latency_ms: float = 800


@dataclass
class Result:
    name: str
    accuracy: float
    missed_outages: int
    cost_per_item_usd: float
    p95_latency_ms: float


def evaluate(name: str, classify: Callable[[str], str], cost_per_call_usd: float = 0.0) -> Result:
    latencies, correct, missed = [], 0, 0
    for text, label in EVAL_SET:
        t0 = time.perf_counter()
        pred = classify(text)
        latencies.append((time.perf_counter() - t0) * 1000)
        correct += pred == label
        missed += label == "outage" and pred != "outage"
    p95 = statistics.quantiles(latencies, n=20)[-1] if len(latencies) > 1 else latencies[0]
    return Result(name, correct / len(EVAL_SET), missed, cost_per_call_usd, p95)


def decide(candidate: Result, baseline: Result, c: Criteria) -> tuple[bool, list[str]]:
    reasons = []
    if candidate.accuracy < c.min_accuracy:
        reasons.append(f"accuracy {candidate.accuracy:.0%} < {c.min_accuracy:.0%}")
    if candidate.accuracy <= baseline.accuracy:
        reasons.append(f"does not beat the baseline ({baseline.accuracy:.0%})")
    if candidate.missed_outages > c.max_missed_outages:
        reasons.append(f"missed {candidate.missed_outages} outage(s)")
    if candidate.cost_per_item_usd > c.max_cost_per_item_usd:
        reasons.append(f"cost ${candidate.cost_per_item_usd:.4f}/item > ${c.max_cost_per_item_usd}")
    if candidate.p95_latency_ms > c.max_p95_latency_ms:
        reasons.append(f"p95 latency {candidate.p95_latency_ms:.0f} ms > {c.max_p95_latency_ms:.0f} ms")
    return not reasons, reasons


def keyword_baseline(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ("down", "500", "timing out", "failing")):
        return "outage"
    if any(w in t for w in ("refund", "charged", "card", "invoice", "subscription")):
        return "billing"
    return "how_to"


def candidate_model(text: str) -> str:
    """Stand-in for an LLM classifier: better on phrasing, still imperfect."""
    t = text.lower()
    if any(w in t for w in ("down", "500", "timing out", "failing", "cannot log in", "blank", "all users", "everyone")):
        return "outage"
    if any(w in t for w in ("refund", "charged", "invoice", "subscription", "tax")):
        return "billing"
    return "how_to"
