#!/bin/bash
echo "=== Installation Script for Support Module Proof ==="
echo "System: $(uname -s)"
echo ""

# Update package lists
echo "1. Updating package lists..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
elif command -v yum &> /dev/null; then
    sudo yum update
elif command -v brew &> /dev/null; then
    brew update
fi

# Install Python dependencies
echo "2. Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install numpy sympy matplotlib pytest
elif command -v pip &> /dev/null; then
    pip install numpy sympy matplotlib pytest
fi

# Install Node.js if not present
echo "3. Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "Node.js not found. Installing..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install Go if not present
echo "4. Checking Go..."
if ! command -v go &> /dev/null; then
    echo "Go not found. Installing..."
    wget https://golang.org/dl/go1.21.0.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
fi

echo ""
echo "=== Installation Complete ==="
echo "Run individual language implementations from src/ directories"
echo "For help: ./scripts/setup/install_all.sh --help"
