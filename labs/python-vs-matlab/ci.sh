#!/usr/bin/env bash
# Python tests, then the same calculation in Python and in MATLAB syntax under GNU Octave.
set -euo pipefail
cd "$(dirname "$0")"
python -m pip install -q -r requirements.txt
python -m unittest discover -s tests -v
if [ -n "${CI:-}" ] && ! command -v octave-cli >/dev/null; then
  sudo apt-get update -qq >/dev/null 2>&1 && sudo apt-get install -y -qq --no-install-recommends octave >/dev/null 2>&1
fi
python compare.py
