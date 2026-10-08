<sub>[← all labs](../../README.md)</sub>

# Secure containers with Podman

> Rootless engine, non-root process, read-only filesystem, no capabilities. Then prove it in CI.

`Podman` · `Containerfile` · `Python`

**Companion to:**
- [Podman - Containerized Deployment & Secure DevOps Pipelines](https://www.linkedin.com/pulse/podman-containerized-deployment-secure-devops-tony-honesto-wfryc/)

## What it shows

- A Containerfile with a pinned base, a fixed non-root UID, a health check and exec-form CMD.
- A policy linter that fails the pipeline before the build on `latest` tags, root users, baked-in secrets and `COPY .`.
- CI builds and runs the image with rootless Podman: `--read-only`, `--cap-drop=ALL`, `no-new-privileges`.
- The run checks the UID inside the container and the health check result.

## Run it

```bash
bash labs/podman-container/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output (from this lab's CI run):

```text
Containerfile: PASS
built race-status:ci
service: {"service": "race-status", "uid": 10001, "version": "1.0.0"}
process runs as uid 10001 inside the container
podman itself runs as host user runner (uid 1001): rootless
healthcheck: healthy
```

## What's in here

| File | Purpose |
|---|---|
| `Containerfile` | The image |
| `app.py` | A tiny status service with a /health endpoint |
| `lint.py` | Containerfile policy checks |
| `samples/Containerfile.bad` | Breaks every rule |
| `ci.sh` | Lint, test, build and a locked-down run |
| `tests/` | Linter tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Python linter | hadolint, Trivy or Checkov config scans |
| Local build | Build in CI, sign (cosign) and push to a registry |
| `podman run` | Quadlet / systemd units, or Kubernetes YAML from `podman generate kube` |
