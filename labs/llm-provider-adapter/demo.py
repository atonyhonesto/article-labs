from adapter import BedrockConverse, Gemini, OpenAIChat, Router
import fake_transport

providers = [BedrockConverse("anthropic.claude-sonnet"), Gemini("gemini-pro"), OpenAIChat("gpt-4o")]
msgs = [{"role": "user", "text": "Lap 41 of 60, tires 22 laps old, caution just came out. Pit?"}]

r = Router(providers, fake_transport.make({"bedrock": [200]}), sleep=lambda s: None)
print("healthy:        ", r.chat("You are a race strategist.", msgs).__dict__)

r = Router(providers, fake_transport.make({"bedrock": [429, 429, 429], "generativelanguage": [503, 200]}), sleep=lambda s: None)
reply = r.chat("You are a race strategist.", msgs)
print("bedrock throttled, gemini blips then answers:", reply.provider, "-", reply.text)
print("attempt log:    ", r.log)
print(f"spend so far:    ${r.spend_usd:.6f}")
