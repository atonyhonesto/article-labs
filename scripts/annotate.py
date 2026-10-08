"""Publish the tail of a lab's output as a GitHub notice annotation, so it shows on the run summary."""
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
lines = [l.rstrip() for l in text.splitlines()][-80:]
body = "\n".join(lines)[-3800:]
esc = body.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
print(f"::notice title=lab output::{esc}")
