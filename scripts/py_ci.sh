#!/usr/bin/env bash
# Shared runner for Python labs: install (if needed) -> unit tests -> demo.
set -euo pipefail
cd "$1"
if [ -f requirements.txt ]; then python -m pip install -q -r requirements.txt; fi
python -m unittest discover -s tests -v
python demo.py
