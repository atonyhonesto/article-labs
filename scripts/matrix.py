"""Emit the GitHub Actions matrix: one job per lab, read from labs/*/lab.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
include = []
for meta in sorted(ROOT.glob("labs/*/lab.json")):
    lab = json.loads(meta.read_text(encoding="utf-8"))
    include.append({
        "lab": meta.parent.name,
        "runtime": lab["runtime"],
        "os": lab.get("os", "ubuntu-latest"),
    })
print(json.dumps({"include": include}))
