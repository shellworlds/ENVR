#!/bin/bash

echo "=== RUNNING SLK8 PROBLEM IN MULTIPLE LANGUAGES ==="
echo "System: $(uname -s) $(uname -r)"
echo "Date: $(date)"
echo ""

# Python
echo "1. PYTHON IMPLEMENTATION"
echo "-----------------------"
cd ~/SLK8-Project
python3 src/slk8_math.py
echo ""

# JavaScript/Node.js
echo "2. JAVASCRIPT/NODE.JS IMPLEMENTATION"
echo "-----------------------------------"
if command -v node >/dev/null 2>&1; then
    node src/slk8.js
else
    echo "Node.js not found, skipping..."
fi
echo ""

# Java
echo "3. JAVA IMPLEMENTATION"
echo "---------------------"
if command -v javac >/dev/null 2>&1 && command -v java >/dev/null 2>&1; then
    cd ~/SLK8-Project/src
    javac SLK8Analysis.java 2>/dev/null
    if [ -f SLK8Analysis.class ]; then
        java SLK8Analysis
        rm SLK8Analysis.class 2>/dev/null
    fi
else
    echo "Java compiler/runtime not found, skipping..."
fi
echo ""

# C++
echo "4. C++ IMPLEMENTATION"
echo "--------------------"
if command -v g++ >/dev/null 2>&1; then
    cd ~/SLK8-Project/src
    g++ -std=c++11 -o slk8_cpp slk8.cpp 2>/dev/null
    if [ -f slk8_cpp ]; then
        ./slk8_cpp
        rm slk8_cpp 2>/dev/null
    fi
else
    echo "g++ compiler not found, skipping..."
fi
echo ""

# Go
echo "5. GO IMPLEMENTATION"
echo "-------------------"
if command -v go >/dev/null 2>&1; then
    cd ~/SLK8-Project/src
    go run slk8.go 2>/dev/null
else
    echo "Go compiler not found, skipping..."
fi
echo ""

echo "=== ALL IMPLEMENTATIONS COMPLETED ==="
echo "Summary: Support(M = ℚ/ℤ) = { (p) | p prime }, not Zariski closed."
