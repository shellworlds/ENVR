#!/bin/bash
# System setup script for SLK8 Project

set -e

echo "=== SLK8 Project Setup ==="
echo "System: $(uname -s) $(uname -r)"
echo "User: $(whoami)"
echo "Date: $(date)"

# Check required tools
echo "Checking required tools..."
tools=("git" "python3" "node" "java" "g++" "go")
for tool in "${tools[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "✓ $tool: $(which $tool)"
    else
        echo "✗ $tool: Not found"
    fi
done

# Install Python dependencies
echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install sympy numpy matplotlib pytest

# Create virtual environment (optional)
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
fi

echo "Setup complete!"
