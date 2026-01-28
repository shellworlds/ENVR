#!/bin/bash

echo "Testing ENVR Module Splitter Implementations"
echo "============================================"

# Python test
echo -e "\n--- Python Test ---"
python3 -c "
import sys
sys.path.append('src')
from module_splitter import ModuleSplitter
splitter = ModuleSplitter(2, 3)
alpha, beta, sigma, rho = splitter.create_standard_maps()
if splitter.verify_theorem(alpha, beta, sigma, rho):
    print('✓ Python: Theorem verified')
else:
    print('✗ Python: Theorem failed')
"

# C++ test (compile and run if g++ available)
echo -e "\n--- C++ Test ---"
if command -v g++ &> /dev/null; then
    mkdir -p bin
    g++ -std=c++11 -o bin/test_cpp src/module_splitter.cpp 2>/dev/null
    if [ -f bin/test_cpp ]; then
        ./bin/test_cpp
    else
        echo "⚠ C++ compilation failed"
    fi
else
    echo "⚠ g++ not installed"
fi

# Java test
echo -e "\n--- Java Test ---"
if command -v javac &> /dev/null && command -v java &> /dev/null; then
    mkdir -p bin
    javac -d bin src/ModuleSplitter.java 2>/dev/null
    if [ $? -eq 0 ]; then
        java -cp bin com.envr.modulesplitter.ModuleSplitter
    else
        echo "⚠ Java compilation failed"
    fi
else
    echo "⚠ Java not installed"
fi

# Go test
echo -e "\n--- Go Test ---"
if command -v go &> /dev/null; then
    go run src/module_splitter.go 2>/dev/null
else
    echo "⚠ Go not installed"
fi

echo -e "\n============================================"
echo "Testing completed"
