from qr import make, decode, modules, survives

URL = "https://github.com/atonyhonesto/article-labs"
FRACTIONS = (0.02, 0.05, 0.08, 0.12, 0.16)
print(f"Payload: {URL}")
print("Share of 20 scans that still decode when a smudge covers part of the code")
print("level  modules  clean  " + "  ".join(f"{f:>4.0%}" for f in FRACTIONS))
for level in "LMQH":
    ok = decode(make(URL, level)) == URL
    rates = [survives(URL, level, f, trials=20) for f in FRACTIONS]
    print(f"  {level}    {modules(URL, level):>2}x{modules(URL, level):<2}   {'yes' if ok else 'no':<5}  "
          + "  ".join(f"{r:>4.0%}" for r in rates))
