"""Rebuild the lab index in README.md from labs/*/lab.json.

    python scripts/build_index.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = [
    ("motorsports-sports", "🏎️ Motorsports & Sports Technology"),
    ("ai-ml", "🤖 AI, Machine Learning & Agents"),
    ("cloud-data-integration", "☁️ Cloud, Data & Integration"),
    ("software-architecture", "🧱 Software Architecture & Engineering Practice"),
    ("engineering-tools", "🛠️ Simulation & Engineering"),
]


def main() -> None:
    labs = []
    for meta in sorted(ROOT.glob("labs/*/lab.json")):
        lab = json.loads(meta.read_text(encoding="utf-8"))
        lab["slug"] = meta.parent.name
        labs.append(lab)
    known = {k for k, _ in THEMES}
    bad = [l["slug"] for l in labs if l["theme"] not in known]
    if bad:
        raise SystemExit(f"unknown theme in: {bad}")

    out = [f"**{len(labs)} labs.** Each folder runs on its own and is tested on every push.", ""]
    for key, label in THEMES:
        rows = [l for l in labs if l["theme"] == key]
        if not rows:
            continue
        out += [f"### {label}", "", "| Lab | What it shows | Stack | Article |", "|---|---|---|---|"]
        for l in rows:
            stack = " · ".join(l["stack"])
            articles = " · ".join(f"[{a['title']}]({a['url']})" for a in l["articles"])
            out.append(f"| [`{l['slug']}`](labs/{l['slug']}) | {l['summary']} | {stack} | {articles} |")
        out.append("")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(r"(<!-- INDEX:START -->\n).*?(<!-- INDEX:END -->)",
                  lambda m: m.group(1) + "\n".join(out) + "\n" + m.group(2), text, flags=re.S)
    text = re.sub(r"labs-\d+-", f"labs-{len(labs)}-", text)
    readme.write_text(text, encoding="utf-8")
    print(f"index rebuilt: {len(labs)} labs")


if __name__ == "__main__":
    main()
