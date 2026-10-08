import unittest
from pathlib import Path
from lint import lint

ROOT = Path(__file__).resolve().parent.parent


class LintTests(unittest.TestCase):
    def test_project_containerfile_passes(self):
        self.assertEqual(lint((ROOT / "Containerfile").read_text()), [])

    def test_bad_containerfile_fails_every_rule(self):
        ids = {rid for rid, _ in lint((ROOT / "samples/Containerfile.bad").read_text())}
        self.assertEqual(ids, {"pinned-base", "non-root", "healthcheck", "no-secrets", "exec-form-cmd", "no-copy-all"})

    def test_digest_pin_accepted(self):
        text = 'FROM python@sha256:abc123\nUSER 1000\nHEALTHCHECK CMD true\nCMD ["x"]\n'
        self.assertEqual(lint(text), [])


if __name__ == "__main__":
    unittest.main()
