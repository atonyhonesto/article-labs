#!/usr/bin/env bash
# Runs on windows-latest: WPF needs Windows to build. The view-model tests would run anywhere.
set -euo pipefail
cd "$(dirname "$0")"
dotnet build WpfMvvm.slnx -c Release -nologo -v q
dotnet test tests/LapTimer.Tests/LapTimer.Tests.csproj -c Release --no-build -nologo --logger "console;verbosity=normal"
