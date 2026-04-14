#!/bin/bash
echo "AE Kryptur Stack - System Validation"
echo "-------------------------------------"
echo "OS: $(lsb_release -ds)"
echo "Kernel: $(uname -r)"
echo "CPU: $(lscpu | grep 'Model name' | cut -d':' -f2 | xargs)"
echo "Memory: $(free -h | awk '/^Mem:/ {print $2}')"
echo "Disk: $(lsblk -o NAME,SIZE,TYPE | grep disk)"
echo "-------------------------------------"
echo "Checking required tools..."
for tool in python3 cargo node go javac g++; do
    if command -v $tool &> /dev/null; then
        echo "[OK] $tool"
    else
        echo "[MISSING] $tool"
    fi
done
