#!/usr/bin/env bash
# Policy check -> unit tests -> rootless Podman build and a locked-down run.
set -euo pipefail
cd "$(dirname "$0")"
python -m unittest discover -s tests -v
python lint.py Containerfile
command -v podman >/dev/null || { echo "podman not installed: skipping the container run"; exit 0; }

# --format docker keeps HEALTHCHECK (the OCI image format has no field for it)
podman build --quiet --format docker -t race-status:ci -f Containerfile . >/dev/null
echo "built race-status:ci"
podman run -d --name race-status -p 8080:8080 \
  --read-only --cap-drop=ALL --security-opt no-new-privileges \
  race-status:ci >/dev/null
trap 'podman rm -f race-status >/dev/null' EXIT
for i in $(seq 1 20); do curl -fs http://127.0.0.1:8080/health >/dev/null 2>&1 && break; sleep 1; done
echo "service: $(curl -fsS http://127.0.0.1:8080/)"
echo "process runs as uid $(podman exec race-status id -u) inside the container"
echo "podman itself runs as host user $(id -un) (uid $(id -u)): rootless"
[ "$(podman exec race-status id -u)" != "0" ]
podman healthcheck run race-status && echo "healthcheck: healthy"
