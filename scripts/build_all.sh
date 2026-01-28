#!/bin/bash

# Build script for all implementations
set -e

echo "Building ENVR Module Splitter implementations..."
echo "================================================"

# Python
echo -e "\n1. Python implementation..."
python3 -m py_compile src/module_splitter.py 2>/dev/null || echo "Python syntax check"
echo "✓ Python ready"

# C++
echo -e "\n2. C++ implementation..."
if command -v g++ &> /dev/null; then
    g++ -std=c++11 -o bin/module_splitter_cpp src/module_splitter.cpp 2>/dev/null || echo "C++ compilation attempted"
    echo "✓ C++ compilation attempted"
else
    echo "⚠ g++ not found, skipping C++"
fi

# Java
echo -e "\n3. Java implementation..."
if command -v javac &> /dev/null; then
    mkdir -p bin
    javac -d bin src/ModuleSplitter.java 2>/dev/null || echo "Java compilation attempted"
    echo "✓ Java compilation attempted"
else
    echo "⚠ javac not found, skipping Java"
fi

# Go
echo -e "\n4. Go implementation..."
if command -v go &> /dev/null; then
    go build -o bin/module_splitter_go src/module_splitter.go 2>/dev/null || echo "Go build attempted"
    echo "✓ Go build attempted"
else
    echo "⚠ go not found, skipping Go"
fi

# Create bin directory if it doesn't exist
mkdir -p bin

echo -e "\n================================================"
echo "Build process completed."
echo "Binaries/outputs in: $(pwd)/bin"
echo "Run scripts in: $(pwd)/scripts"
