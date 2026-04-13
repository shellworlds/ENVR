#!/bin/bash
# PT-OF 1.6 Dependency Installer for Ubuntu 24.04
set -e

echo "Installing system packages..."
sudo apt update
sudo apt install -y python3.12-venv python3.12-dev libssl-dev libffi-dev cargo pkg-config docker.io docker-compose htop iotop nvme-cli

echo "Creating Python virtual environment..."
python3.12 -m venv ptof_env
source ptof_env/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip
pip install qcodes numpy scipy matplotlib torch torchvision fastapi uvicorn pydantic motor asyncpg sqlalchemy pyvisa pynq pytest black isort

echo "Dependency installation complete."
