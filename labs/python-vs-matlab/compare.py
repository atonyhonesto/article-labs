"""Run both versions and compare. Octave is optional locally; CI installs it."""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def parse(text):
    return {k: float(v) for k, v in (line.split("=") for line in text.strip().splitlines())}


py = parse(subprocess.run([sys.executable, "analysis.py"], cwd=HERE, capture_output=True, text=True, check=True).stdout)
octave = shutil.which("octave-cli") or shutil.which("octave")
if not octave:
    print("Octave not installed: Python results only")
    for k, v in py.items():
        print(f"  {k:<12} {v:>12.4f}")
    sys.exit(0)

m = parse(subprocess.run([octave, "--quiet", "--no-window-system", "analysis.m"], cwd=HERE, capture_output=True, text=True, check=True).stdout)
print(f"  {'result':<12} {'Python':>12} {'MATLAB/Octave':>14}  match")
ok = True
for k in py:
    same = abs(py[k] - m[k]) <= 1e-6 * max(1, abs(py[k]))
    ok &= same
    print(f"  {k:<12} {py[k]:>12.4f} {m[k]:>14.4f}  {'yes' if same else 'NO'}")
sys.exit(0 if ok else 1)
