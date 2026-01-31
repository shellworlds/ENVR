#!/bin/bash

echo "=== Building C++ Quantum Simulator ==="

# Create build directory
mkdir -p build/cpp
cd build/cpp

# Check compiler
if command -v g++ &> /dev/null; then
    COMPILER="g++"
elif command -v clang++ &> /dev/null; then
    COMPILER="clang++"
else
    echo "Error: C++ compiler not found. Install g++ or clang++"
    exit 1
fi

echo "Using compiler: $COMPILER"

# Compile with optimizations
$COMPILER -std=c++17 -O3 -march=native -pthread \
    ../../src/cpp/quantum_simulator.cpp \
    -o quantum_simulator

# Check if compilation succeeded
if [ $? -eq 0 ]; then
    echo "Compilation successful!"
    echo "Binary created: build/cpp/quantum_simulator"
    
    # Run the compiled program
    echo ""
    echo "=== Running C++ Quantum Simulator ==="
    ./quantum_simulator
else
    echo "Compilation failed!"
    exit 1
fi
