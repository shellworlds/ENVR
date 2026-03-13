#!/usr/bin/env bash
# SN-112BA System Check Script
# Run on Lenovo (Ubuntu), Mac, or Windows (WSL/Git Bash) to verify OS and specs before running POC.
# Main developer: shellworlds

set -e
REPORT="sn112ba_system_report.txt"
echo "SN-112BA System Check - $(date -Iseconds 2>/dev/null || date)" | tee "$REPORT"

detect_os() {
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "OS: $PRETTY_NAME ($ID $VERSION_ID)" | tee -a "$REPORT"
    echo "Kernel: $(uname -r)" | tee -a "$REPORT"
  elif command -v sw_vers &>/dev/null; then
    echo "OS: $(sw_vers -productName) $(sw_vers -productVersion)" | tee -a "$REPORT"
    echo "Kernel: $(uname -r)" | tee -a "$REPORT"
  else
    echo "OS: $(uname -s) $(uname -r)" | tee -a "$REPORT"
  fi
  echo "Arch: $(uname -m)" | tee -a "$REPORT"
}

echo "--- Platform ---" | tee -a "$REPORT"
detect_os
if [ -f /sys/devices/virtual/dmi/id/product_family 2>/dev/null ]; then
  echo "Product: $(cat /sys/devices/virtual/dmi/id/product_family 2>/dev/null)" | tee -a "$REPORT"
fi
if [ -f /sys/devices/virtual/dmi/id/sys_vendor 2>/dev/null ]; then
  echo "Vendor: $(cat /sys/devices/virtual/dmi/id/sys_vendor 2>/dev/null)" | tee -a "$REPORT"
fi

echo "--- Memory ---" | tee -a "$REPORT"
if command -v free &>/dev/null; then
  free -h | tee -a "$REPORT"
else
  echo "free not available" | tee -a "$REPORT"
fi

echo "--- Storage ---" | tee -a "$REPORT"
if command -v df &>/dev/null; then
  df -h . 2>/dev/null | tee -a "$REPORT"
fi

echo "--- Python ---" | tee -a "$REPORT"
for py in python3 python; do
  if command -v "$py" &>/dev/null; then
    echo "$py: $($py --version 2>&1)" | tee -a "$REPORT"
    break
  fi
done

echo "--- Node ---" | tee -a "$REPORT"
if command -v node &>/dev/null; then
  echo "node: $(node --version)" | tee -a "$REPORT"
fi
if command -v npm &>/dev/null; then
  echo "npm: $(npm --version)" | tee -a "$REPORT"
fi

echo "--- Go ---" | tee -a "$REPORT"
if command -v go &>/dev/null; then
  echo "go: $(go version)" | tee -a "$REPORT"
fi

echo "--- Java ---" | tee -a "$REPORT"
if command -v java &>/dev/null; then
  echo "java: $(java -version 2>&1 | head -1)" | tee -a "$REPORT"
fi

echo "--- C++ (g++) ---" | tee -a "$REPORT"
if command -v g++ &>/dev/null; then
  echo "g++: $(g++ --version | head -1)" | tee -a "$REPORT"
fi

echo "--- Git ---" | tee -a "$REPORT"
if command -v git &>/dev/null; then
  echo "git: $(git --version)" | tee -a "$REPORT"
  echo "user: $(git config user.name 2>/dev/null || echo not set)" | tee -a "$REPORT"
fi

echo "--- Report saved to $REPORT ---"
