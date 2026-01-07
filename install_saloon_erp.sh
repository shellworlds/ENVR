#!/bin/bash
echo "Saloon ERP Installation Script"
echo "=============================="

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux detected"
    sudo apt update
    sudo apt install -y python3 python3-pip nodejs npm default-jdk g++ golang
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected"
    brew install python node openjdk gcc go
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Windows detected"
    echo "Install Python, Node.js, Java, C++ tools manually"
else
    echo "Unknown OS"
fi

# Install Python packages
pip3 install flask requests pandas numpy

# Install Node.js packages
npm init -y
npm install express react react-dom

echo "Installation complete"
echo "Run: python3 saloon_erp.py"
