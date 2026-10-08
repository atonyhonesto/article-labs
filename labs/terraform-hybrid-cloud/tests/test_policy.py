"""Policy-as-code checks that run without Terraform installed: conventions a reviewer would otherwise catch."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TF = sorted(ROOT.rglob("*.tf"))


class PolicyTests(unittest.TestCase):
    def test_every_provider_is_version_pinned(self):
        for f in TF:
            text = f.read_text()
            sources = re.findall(r'source\s*=\s*"hashicorp/\w+"', text)
            pinned = re.findall(r'source\s*=\s*"hashicorp/\w+"\s*\n\s*version\s*=\s*"~> \d+\.\d+"', text)
            self.assertEqual(len(sources), len(pinned), f"unpinned provider in {f}")

    def test_every_environment_tags_its_resources(self):
        for env in (ROOT / "envs").iterdir():
            text = (env / "main.tf").read_text()
            for key in ("environment", "owner", "managed_by"):
                self.assertIn(key, text, f"{env.name} is missing tag {key}")

    def test_web_app_enforces_https_and_tls12(self):
        text = (ROOT / "modules/azure-app/main.tf").read_text()
        self.assertIn("https_only          = true", text)
        self.assertIn('minimum_tls_version = "1.2"', text)

    def test_prod_is_multi_az_and_not_on_basic_sku(self):
        text = (ROOT / "envs/prod/main.tf").read_text()
        self.assertGreaterEqual(text.count("us-east-2"), 4)       # region + 3 AZs
        self.assertNotIn('sku    = "B1"', text)


if __name__ == "__main__":
    unittest.main()
