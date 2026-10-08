<sub>[← all labs](../../README.md)</sub>

# Python vs. MATLAB: the same calculation twice

> The syntax differs in small, important ways. The answers shouldn't.

`Python` · `NumPy` · `SciPy` · `GNU Octave`

**Companion to:**
- [Python vs MATLAB](https://www.linkedin.com/pulse/python-vs-matlab-tony-honesto-4bg9c/)
- [MathWorks - MATLAB Onramp - Interactive Introduction](https://www.linkedin.com/pulse/matlab-onramp-free-interactive-introduction-tony-honesto-yg5pc/)

## What it shows

- Three common calculations: trapezoidal integration, an FFT peak and a log-linear curve fit.
- `analysis.py` (NumPy) and `analysis.m` (MATLAB syntax) side by side: 0- vs 1-based indexing, argument order, one-sided spectra.
- CI installs GNU Octave, runs both and checks the results match.

## Run it

```bash
bash labs/python-vs-matlab/ci.sh   # installs Octave in CI
# or locally:
python compare.py           # Python only if Octave isn't installed
octave --quiet analysis.m
```

Real output (from this lab's CI run):

```text
  result             Python  MATLAB/Octave  match
  distance_m       599.7001       599.7001  yes
  dominant_hz       12.5000        12.5000  yes
  tau_s              3.1970         3.1970  yes
  mean_speed        60.0000        60.0000  yes
```

## What's in here

| File | Purpose |
|---|---|
| `analysis.py` | NumPy version |
| `analysis.m` | MATLAB / Octave version |
| `compare.py` | Runs both and compares |
| `tests/` | Checks the Python results |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| GNU Octave | MATLAB itself, with toolboxes |
| Three calculations | Full analysis scripts; the MATLAB Engine API for Python can call one from the other |
| Synthetic signals | Logged test data |
