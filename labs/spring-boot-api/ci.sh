#!/usr/bin/env bash
# Build and test, then start the jar and call it like a client would.
set -euo pipefail
cd "$(dirname "$0")"
mvn -B -q verify
java -jar target/spring-boot-api-1.0.0.jar > app.log 2>&1 &
pid=$!
trap 'kill $pid 2>/dev/null || true' EXIT
for i in $(seq 1 60); do curl -fsS localhost:8080/actuator/health >/dev/null 2>&1 && break; sleep 1; done
call() { echo "\$ curl $*"; curl -sS -w '  <- HTTP %{http_code}\n' "$@"; }
call -X POST localhost:8080/api/entries -H 'Content-Type: application/json' -d '{"number":24,"driver":"A. Driver","team":"Team Green"}'
call -X POST localhost:8080/api/entries -H 'Content-Type: application/json' -d '{"number":150,"driver":"","team":"X"}'
call localhost:8080/api/entries
call localhost:8080/api/entries/7
