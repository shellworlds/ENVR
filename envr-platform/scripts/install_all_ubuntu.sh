#!/usr/bin/env bash
# One-shot Ubuntu install for ENVR toolchain (sudo required)

set -euo pipefail
sudo apt-get update -qq
sudo apt-get install -y \
  python3 python3-pip python3-venv \
  nodejs npm \
  git openssh-client curl ca-certificates \
  build-essential \
  default-jdk-headless \
  golang-go \
  unzip rsync \
  jq \
  docker.io \
  || true

echo "Core packages installed. Optional: sudo usermod -aG docker $USER then re-login for Docker."
pip3 install --user --break-system-packages virtualenv 2>/dev/null || pip3 install --user virtualenv 2>/dev/null || true
echo "Done. Run ./scripts/verify_toolchain.sh"
