#!/usr/bin/env bash
set -euo pipefail
REPORT=${1:-system_report.txt}
CPU=$(lscpu | awk -F: '/Model name/{print $2}' | xargs || true)
RAM=$(awk '/MemTotal/{printf "%.2f GB", $2/1024/1024}' /proc/meminfo)
OS=$(grep PRETTY_NAME /etc/os-release | cut -d= -f2- | tr -d '"')
TOOLS=(git gh python3 pip3 node npm java javac go gcc g++ docker kubectl qiskit)
{
  echo "ENVR System Report"
  echo "Generated: $(date -u)"
  echo "OS: $OS"
  echo "CPU: ${CPU:-unknown}"
  echo "RAM: $RAM"
  echo
  echo "Tool Availability"
  for t in "${TOOLS[@]}"; do
    if command -v "$t" >/dev/null 2>&1; then
      echo "[OK] $t"
    else
      echo "[MISS] $t"
    fi
  done
} | tee "$REPORT"
