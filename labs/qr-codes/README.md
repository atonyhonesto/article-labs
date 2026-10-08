<sub>[← all labs](../../README.md)</sub>

# QR codes: how much damage each level survives

> Error correction is a trade: every level that survives more damage needs a bigger code.

`Python` · `OpenCV`

**Companion to:**
- [Python + QR Codes](https://www.linkedin.com/pulse/python-qr-codes-tony-honesto-98olc/)

## What it shows

- Generates the same URL at each error-correction level (L, M, Q, H) and decodes it with OpenCV.
- Higher levels need more modules (a larger symbol) for the same data.
- Paints a smudge over part of the code, like a sticker or scuff, and counts how many scans still decode.

## Run it

```bash
bash labs/qr-codes/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output (from this lab's CI run):

```text
Payload: https://github.com/atonyhonesto/article-labs
Share of 20 scans that still decode when a smudge covers part of the code
level  modules  clean    2%    5%    8%   12%   16%
  L    33x33   yes    100%    0%    0%    0%    0%
  M    37x37   yes    100%  100%   70%    0%    0%
  Q    37x37   yes    100%  100%  100%   20%    0%
  H    41x41   yes    100%  100%  100%  100%   60%
```

## What's in here

| File | Purpose |
|---|---|
| `qr.py` | Encode, decode and damage, with OpenCV's QR encoder and detector |
| `demo.py` | Survival table across levels and damage sizes |
| `tests/` | Round trip, size and damage tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| OpenCV encoder | `qrcode` or `segno` for styling, logos and print-ready SVG |
| Synthetic smudge | Phone cameras, glare, curvature and print quality |
| Level chosen by hand | H for printed labels and logos, M for screens |
