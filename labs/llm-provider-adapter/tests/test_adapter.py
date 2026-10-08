import unittest

import fake_transport
from adapter import AllProvidersFailed, BedrockConverse, Gemini, OpenAIChat, Router

MSGS = [{"role": "user", "text": "hi"}]


class AdapterTests(unittest.TestCase):
    def test_request_shapes(self):
        self.assertIn("inferenceConfig", BedrockConverse("m").body("s", MSGS, 10))
        self.assertEqual(Gemini("m").body("s", [{"role": "assistant", "text": "x"}], 10)["contents"][0]["role"], "model")
        self.assertEqual(OpenAIChat("m").body("s", MSGS, 10)["messages"][0], {"role": "system", "content": "s"})

    def test_retries_with_backoff_then_succeeds(self):
        delays = []
        r = Router([BedrockConverse("m")], fake_transport.make({"bedrock": [429, 503, 200]}), sleep=delays.append)
        self.assertEqual(r.chat("s", MSGS).provider, "bedrock")
        self.assertEqual(delays, [0.2, 0.4])

    def test_client_errors_skip_straight_to_fallback(self):
        r = Router([BedrockConverse("m"), OpenAIChat("m")], fake_transport.make({"bedrock": [400], "openai": [200]}),
                   sleep=lambda s: None)
        self.assertEqual(r.chat("s", MSGS).provider, "openai")
        self.assertEqual([x[0] for x in r.log], ["bedrock", "openai"])

    def test_cost_accounting(self):
        r = Router([OpenAIChat("m")], fake_transport.make({"openai": [200]}))
        rep = r.chat("s", MSGS)
        self.assertAlmostEqual(rep.cost_usd, 125 / 1e6 * 2.5 + 15 / 1e6 * 10)

    def test_all_fail(self):
        r = Router([Gemini("m")], fake_transport.make({"generativelanguage": [500]}), sleep=lambda s: None)
        with self.assertRaises(AllProvidersFailed):
            r.chat("s", MSGS)


if __name__ == "__main__":
    unittest.main()
