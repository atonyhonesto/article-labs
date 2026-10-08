#!/usr/bin/env bash
set -euo pipefail
bash "$(dirname "$0")/../../scripts/py_ci.sh" "$(dirname "$0")"
