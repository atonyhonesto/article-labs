"""Audit robots.txt files for AI crawler access using only the standard library.

robots.txt is a request, not a lock: well-behaved crawlers honour it, others don't.
The audit answers three questions for each site:
  1. Which AI crawlers may fetch a given path?
  2. Did the site rely on the '*' group by accident (no explicit rule for the bot)?
  3. Are search crawlers still allowed, so blocking AI doesn't cost search traffic?
"""
from __future__ import annotations

from dataclasses import dataclass
from urllib.robotparser import RobotFileParser

# User-agent tokens published by each operator (training vs. retrieval differs per vendor).
AI_CRAWLERS = {
    "GPTBot": "OpenAI (training)",
    "OAI-SearchBot": "OpenAI (search)",
    "ChatGPT-User": "OpenAI (user-triggered fetch)",
    "ClaudeBot": "Anthropic (training)",
    "Claude-User": "Anthropic (user-triggered fetch)",
    "Claude-SearchBot": "Anthropic (search)",
    "CCBot": "Common Crawl (training corpus)",
    "Google-Extended": "Google (Gemini training opt-out token)",
    "PerplexityBot": "Perplexity",
    "Bytespider": "ByteDance",
    "Applebot-Extended": "Apple (training opt-out token)",
}
SEARCH_CRAWLERS = ["Googlebot", "Bingbot"]


@dataclass
class Row:
    agent: str
    operator: str
    allowed: bool
    explicit: bool          # the file names this agent rather than falling back to '*'


def parse(text: str) -> RobotFileParser:
    rp = RobotFileParser()
    rp.parse(text.splitlines())
    return rp


def named_agents(text: str) -> set[str]:
    return {line.split(":", 1)[1].strip().lower()
            for line in text.splitlines() if line.lower().startswith("user-agent:")}


def audit(text: str, url: str = "https://site.example/articles/1") -> tuple[list[Row], dict[str, bool]]:
    rp, named = parse(text), named_agents(text)
    rows = [Row(a, op, rp.can_fetch(a, url), a.lower() in named) for a, op in AI_CRAWLERS.items()]
    search = {a: rp.can_fetch(a, url) for a in SEARCH_CRAWLERS}
    return rows, search


def findings(rows: list[Row], search: dict[str, bool], text: str) -> list[str]:
    out = []
    implicit = [r.agent for r in rows if r.allowed and not r.explicit]
    if implicit:
        out.append(f"{len(implicit)} AI crawlers allowed only by default ('*'): {', '.join(implicit[:4])}...")
    if "anthropic-ai" in named_agents(text) and not any(r.agent == "ClaudeBot" and r.explicit for r in rows):
        out.append("blocks 'anthropic-ai', a retired token; ClaudeBot is not named")
    if not any(search.values()):
        out.append("search crawlers are blocked from this path too, so it drops out of search results")
    blocked_training = [r.agent for r in rows if not r.allowed and "training" in r.operator]
    if blocked_training and all(search.values()):
        out.append(f"blocks training ({', '.join(blocked_training)}) while keeping search open")
    return out
