"""One interface over several LLM APIs, with retries, fallback and cost tracking.

Each provider class only knows how to turn a chat into ITS request body and
parse ITS response. Everything else (retries on 429/5xx with backoff, falling
back to the next provider, counting tokens and cost) lives once, in `Router`.

Request shapes follow the public APIs: Amazon Bedrock Converse, Google Gemini
`generateContent`, and OpenAI-style Chat Completions. The HTTP call is injected,
so tests and this demo run against a fake transport with no keys.
Prices are illustrative placeholders; set them from your provider's price sheet.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

Transport = Callable[[str, dict], tuple[int, dict]]     # (url, json body) -> (status, json response)


@dataclass
class Reply:
    text: str
    provider: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class Provider:
    name = "base"
    price_in_per_m = 0.0
    price_out_per_m = 0.0

    def __init__(self, model: str):
        self.model = model

    def url(self) -> str: ...
    def body(self, system: str, messages: list[dict], max_tokens: int) -> dict: ...
    def parse(self, resp: dict) -> tuple[str, int, int]: ...


class BedrockConverse(Provider):
    name, price_in_per_m, price_out_per_m = "bedrock", 3.0, 15.0

    def url(self):
        return f"https://bedrock-runtime.us-east-1.amazonaws.com/model/{self.model}/converse"

    def body(self, system, messages, max_tokens):
        return {"system": [{"text": system}],
                "messages": [{"role": m["role"], "content": [{"text": m["text"]}]} for m in messages],
                "inferenceConfig": {"maxTokens": max_tokens}}

    def parse(self, r):
        return (r["output"]["message"]["content"][0]["text"], r["usage"]["inputTokens"], r["usage"]["outputTokens"])


class Gemini(Provider):
    name, price_in_per_m, price_out_per_m = "gemini", 1.25, 5.0

    def url(self):
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def body(self, system, messages, max_tokens):
        return {"systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["text"]}]}
                             for m in messages],
                "generationConfig": {"maxOutputTokens": max_tokens}}

    def parse(self, r):
        return (r["candidates"][0]["content"]["parts"][0]["text"],
                r["usageMetadata"]["promptTokenCount"], r["usageMetadata"]["candidatesTokenCount"])


class OpenAIChat(Provider):
    name, price_in_per_m, price_out_per_m = "openai", 2.5, 10.0

    def url(self):
        return "https://api.openai.com/v1/chat/completions"

    def body(self, system, messages, max_tokens):
        return {"model": self.model, "max_tokens": max_tokens,
                "messages": [{"role": "system", "content": system}] + [{"role": m["role"], "content": m["text"]} for m in messages]}

    def parse(self, r):
        return (r["choices"][0]["message"]["content"], r["usage"]["prompt_tokens"], r["usage"]["completion_tokens"])


class AllProvidersFailed(RuntimeError):
    pass


@dataclass
class Router:
    providers: list[Provider]
    transport: Transport
    retries: int = 2
    base_delay_s: float = 0.2
    sleep: Callable[[float], None] = time.sleep
    spend_usd: float = 0.0
    log: list = field(default_factory=list)

    def chat(self, system: str, messages: list[dict], max_tokens: int = 512) -> Reply:
        for p in self.providers:
            for attempt in range(self.retries + 1):
                status, resp = self.transport(p.url(), p.body(system, messages, max_tokens))
                self.log.append((p.name, attempt, status))
                if status == 200:
                    text, tin, tout = p.parse(resp)
                    cost = tin / 1e6 * p.price_in_per_m + tout / 1e6 * p.price_out_per_m
                    self.spend_usd += cost
                    return Reply(text, p.name, tin, tout, cost)
                if status in (429, 500, 502, 503, 529) and attempt < self.retries:
                    self.sleep(self.base_delay_s * 2 ** attempt)        # exponential backoff
                    continue
                break                                                   # 4xx or out of retries: next provider
        raise AllProvidersFailed(f"every provider failed: {self.log}")
