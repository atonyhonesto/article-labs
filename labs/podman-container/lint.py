"""A Containerfile policy check that runs before the build, the cheap place to catch problems.

Rules mirror what hadolint / Trivy config scans / a security reviewer would flag.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RULES = [
    ("pinned-base", "base image must name a specific tag, not 'latest' or nothing",
     lambda lines: all(re.search(r":(?!latest\b)[\w.\-]+(@sha256:\w+)?$", l.split()[1]) or "@sha256:" in l
                       for l in lines if l.upper().startswith("FROM "))),
    ("non-root", "final stage must switch to a non-root USER",
     lambda lines: any(l.upper().startswith("USER ") and l.split()[1] not in ("root", "0") for l in lines)),
    ("healthcheck", "image should declare a HEALTHCHECK",
     lambda lines: any(l.upper().startswith("HEALTHCHECK ") for l in lines)),
    ("no-secrets", "no passwords, tokens or keys baked into ENV/ARG",
     lambda lines: not any(re.match(r"(ENV|ARG)\s+.*(PASSWORD|SECRET|TOKEN|API_KEY)\s*=", l, re.I) for l in lines)),
    ("exec-form-cmd", "CMD/ENTRYPOINT in exec form so signals reach the process",
     lambda lines: all(l.split(None, 1)[1].lstrip().startswith("[") for l in lines
                       if l.upper().startswith(("CMD ", "ENTRYPOINT ")))),
    ("no-copy-all", "avoid COPY . (copies secrets and junk unless .containerignore is perfect)",
     lambda lines: not any(re.match(r"COPY\s+(--\S+\s+)*\.\s", l) for l in lines)),
]


def logical_lines(text: str) -> list[str]:
    joined = re.sub(r"\\\n\s*", " ", text)
    return [l.strip() for l in joined.splitlines() if l.strip() and not l.strip().startswith("#")]


def lint(text: str) -> list[tuple[str, str]]:
    lines = logical_lines(text)
    return [(rid, msg) for rid, msg, ok in RULES if not ok(lines)]


if __name__ == "__main__":
    failed = False
    for path in sys.argv[1:] or ["Containerfile"]:
        problems = lint(Path(path).read_text())
        print(f"{path}: {'PASS' if not problems else f'{len(problems)} problem(s)'}")
        for rid, msg in problems:
            print(f"  [{rid}] {msg}")
        failed |= bool(problems) and not path.endswith(".bad")
    sys.exit(1 if failed else 0)
