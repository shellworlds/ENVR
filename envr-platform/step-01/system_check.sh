#!/usr/bin/env bash
# Step 01: System and OS specification check (Linux/Ubuntu primary)
# Lenovo ThinkPad class: AMD Gen5, 32GB RAM, 1TB SSD typical target

set -euo pipefail

echo "=== ENVR Step 01: System check ==="
echo "Timestamp (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

echo "--- OS ---"
if [[ -f /etc/os-release ]]; then
  # shellcheck source=/dev/null
  . /etc/os-release
  echo "NAME: ${PRETTY_NAME:-$NAME}"
  echo "VERSION: ${VERSION:-unknown}"
else
  uname -a
fi
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo ""

echo "--- CPU ---"
if [[ -r /proc/cpuinfo ]]; then
  grep -m1 "model name" /proc/cpuinfo 2>/dev/null || grep -m1 "^model name" /proc/cpuinfo 2>/dev/null || true
  echo "CPU cores (online): $(nproc 2>/dev/null || echo n/a)"
fi
if command -v lscpu >/dev/null 2>&1; then
  lscpu | grep -E "^(Architecture|CPU\(s\)|Model name|Thread|Socket)" || true
fi
echo ""

echo "--- Memory ---"
if [[ -r /proc/meminfo ]]; then
  grep -E "MemTotal|MemAvailable|SwapTotal" /proc/meminfo
fi
echo ""

echo "--- Primary disk (/) ---"
df -h / 2>/dev/null || true
echo ""

echo "--- Shell ---"
echo "SHELL: ${SHELL:-unknown}"
echo "Script runner: bash ${BASH_VERSION:-unknown}"
echo ""

echo "--- Git (if installed) ---"
if command -v git >/dev/null 2>&1; then
  git --version
  echo "Global user.name: $(git config --global user.name 2>/dev/null || echo '(not set)')"
  echo "Global user.email: $(git config --global user.email 2>/dev/null || echo '(not set)')"
else
  echo "git not found"
fi
echo ""

echo "=== Step 01 complete. Save this output for POC baseline. ==="
