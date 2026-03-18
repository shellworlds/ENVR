#!/usr/bin/env bash
set -euo pipefail
echo "=== Toolchain verification ==="
for cmd in python3 pip3 node npm git curl java javac go g++ make docker jq; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "OK $cmd: $(command -v $cmd)"
  else
    echo "MISSING $cmd"
  fi
done
python3 --version
node --version 2>/dev/null || true
go version 2>/dev/null || true
java --version 2>/dev/null | head -1 || true
