import unittest
from pathlib import Path
from audit import audit, findings, named_agents

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


def load(name):
    return (SAMPLES / name).read_text()


class AuditTests(unittest.TestCase):
    def test_news_site_blocks_named_training_bots(self):
        rows, search = audit(load("news-site.txt"))
        by = {r.agent: r for r in rows}
        for bot in ("GPTBot", "CCBot", "Google-Extended", "ClaudeBot"):
            self.assertFalse(by[bot].allowed)
            self.assertTrue(by[bot].explicit)
        self.assertTrue(by["PerplexityBot"].allowed)
        self.assertTrue(all(search.values()))

    def test_team_site_allows_everything_implicitly(self):
        rows, _ = audit(load("team-site.txt"))
        self.assertTrue(all(r.allowed and not r.explicit for r in rows))
        rows, _ = audit(load("team-site.txt"), "https://site.example/telemetry/raw/lap1.csv")
        self.assertFalse(any(r.allowed for r in rows))

    def test_retired_token_is_flagged(self):
        text = load("docs-site.txt")
        rows, search = audit(text, "https://site.example/docs/intro")
        self.assertTrue(search["Googlebot"])
        self.assertIn("anthropic-ai", named_agents(text))
        self.assertTrue(any("retired" in f for f in findings(rows, search, text)))


if __name__ == "__main__":
    unittest.main()
