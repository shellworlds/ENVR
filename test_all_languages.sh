#!/bin/bash
echo "Testing Multi-Language Quantum Showcase"
echo "========================================"

# Test Python
echo -n "1. Python... "
cd languages/python
python3 -c "import sys; print('Python', sys.version.split()[0])" && echo "✓"
cd ../..

# Test Shell
echo -n "2. Shell... "
cd languages/shell
bash -n quantum_ops.sh && echo "✓ Syntax OK"
cd ../..

# Test C compilation
echo -n "3. C Compilation... "
cd languages/c
make clean 2>/dev/null
make 2>/dev/null && echo "✓ Compiled"
cd ../..

# Test JavaScript
echo -n "4. JavaScript... "
if command -v node &> /dev/null; then
    cd languages/javascript
    node -c quantum-circuit.js && echo "✓ Syntax OK"
    cd ../..
else
    echo "✗ Node.js not installed"
fi

# Test Java compilation
echo -n "5. Java Compilation... "
if command -v javac &> /dev/null; then
    cd languages/java
    javac QuantumSimulator.java 2>/dev/null && echo "✓ Compiled"
    cd ../..
else
    echo "✗ Java not installed"
fi

# Test Go
echo -n "6. Go... "
if command -v go &> /dev/null; then
    cd languages/go
    go vet quantum.go 2>/dev/null && echo "✓ No issues"
    cd ../..
else
    echo "✗ Go not installed"
fi

echo "========================================"
echo "Test completed!"
echo "View implementations in: languages/"
