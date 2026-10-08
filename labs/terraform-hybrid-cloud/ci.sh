#!/usr/bin/env bash
# Validate every environment without credentials, then run the policy checks.
set -euo pipefail
cd "$(dirname "$0")"
for env in envs/*/; do
  echo "== $env"
  terraform -chdir="$env" init -backend=false -input=false -no-color >/dev/null
  terraform -chdir="$env" validate -no-color
done
python -m unittest discover -s tests -v
