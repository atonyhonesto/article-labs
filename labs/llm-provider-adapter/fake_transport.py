"""A fake HTTP layer that answers in each provider's real response format."""
from __future__ import annotations


def make(script: dict[str, list[int]]):
    """script maps a URL fragment to the status codes it returns, in order (200 = success)."""
    calls = {k: 0 for k in script}

    def transport(url: str, body: dict):
        key = next(k for k in script if k in url)
        codes = script[key]
        status = codes[min(calls[key], len(codes) - 1)]
        calls[key] += 1
        if status != 200:
            return status, {"error": {"code": status}}
        if "bedrock" in url:
            return 200, {"output": {"message": {"content": [{"text": "Bedrock says: box this lap."}]}},
                         "usage": {"inputTokens": 120, "outputTokens": 18}}
        if "generativelanguage" in url:
            return 200, {"candidates": [{"content": {"parts": [{"text": "Gemini says: stay out."}]}}],
                         "usageMetadata": {"promptTokenCount": 118, "candidatesTokenCount": 12}}
        return 200, {"choices": [{"message": {"content": "OpenAI says: box next lap."}}],
                     "usage": {"prompt_tokens": 125, "completion_tokens": 15}}

    return transport
