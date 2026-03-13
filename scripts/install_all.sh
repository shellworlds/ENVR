#!/usr/bin/env bash
# SN-112BA one-command install. Main developer: shellworlds.
# Lenovo/Ubuntu, Mac, Windows (WSL or Git Bash): run from project root.

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "SN-112BA install at $ROOT"

if command -v python3 &>/dev/null; then
  echo "Installing Python deps..."
  pip3 install -r requirements.txt --user 2>/dev/null || pip install -r requirements.txt --user 2>/dev/null || true
fi

if [ -d "api" ] && command -v npm &>/dev/null; then
  echo "Installing API deps..."
  (cd api && npm install --no-audit --no-fund)
fi

if [ -d "dashboard" ] && command -v npm &>/dev/null; then
  echo "Installing dashboard deps..."
  (cd dashboard && npm install --no-audit --no-fund)
fi

if [ -d "next-app" ] && command -v npm &>/dev/null; then
  echo "Installing Next deps..."
  (cd next-app && npm install --no-audit --no-fund)
fi

echo "SN-112BA install complete. Run: ./scripts/system_check.sh"
