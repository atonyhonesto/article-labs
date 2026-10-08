#!/usr/bin/env bash
# 1) the real project must pass both gates; 2) the same project plus one bad file must fail.
set -euo pipefail
cd "$(dirname "$0")"
mvn -B -q verify
echo "== quality gate passed: checkstyle clean, tests green, line coverage >= 80%"
java -cp target/classes dev.honesto.standards.Demo

tmp=$(mktemp -d)
cp -r pom.xml checkstyle.xml src "$tmp"
cp samples/BadExample.java "$tmp/src/main/java/dev/honesto/standards/"
echo "== same build with samples/BadExample.java added:"
if (cd "$tmp" && mvn -B -o checkstyle:check > build.log 2>&1); then
  echo "expected the gate to fail"; exit 1
fi
grep -E '^\[(WARN|WARNING|ERROR)\] .*BadExample' "$tmp/build.log" | sed -E 's#^.*/(BadExample\.java)#  \1#' | sort -u
echo "== gate failed as expected"
