# System Specifications for Quantum JV Platform

## Hardware
- Device: Lenovo ThinkPad P14s Gen 5 AMD
- Processor: AMD Ryzen 7 PRO 8840HS w/ Radeon 780M Graphics
- RAM: 32 GB (27Gi available)
- Storage: 1 TB SSD (709G available)
- OS: Ubuntu 24.04.3 LTS (Noble Numbat)

## Software Requirements Verified
- [✓] Python 3.12.7
- [✓] Node.js v20.20.0
- [✓] Java 21.0.9
- [✓] Git 2.43.0
- [✓] SSH Authentication to GitHub (Confirmed: BorelSigmaInc)

## Installation Commands for Other Systems

### MacOS
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11 node@20 openjdk@17 git
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install python git nodejs openjdk17 -y
refreshenv
sudo apt update
sudo apt install -y python3-pip nodejs npm default-jdk git curl wget build-essential
Next Step Verification
bash
chmod +x scripts/verify_requirements.sh
./scripts/verify_requirements.sh
