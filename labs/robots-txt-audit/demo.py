from pathlib import Path
from audit import audit, findings

URL = "https://site.example/articles/1"
for f in sorted(Path(__file__).with_name("samples").glob("*.txt")):
    text = f.read_text()
    rows, search = audit(text, URL)
    allowed = sum(r.allowed for r in rows)
    print(f"{f.stem:<10} AI crawlers allowed {allowed:>2}/{len(rows)}   search: "
          + ", ".join(f"{k} {'yes' if v else 'no'}" for k, v in search.items()))
    for line in findings(rows, search, text):
        print(f"           - {line}")
