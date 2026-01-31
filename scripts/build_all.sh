#!/bin/bash

echo "=== Building All Quantum Components ==="
echo "Timestamp: $(date)"
echo ""

# Create build directory
mkdir -p build

# Build C++ component
echo "1. Building C++ Quantum Simulator..."
./scripts/build_cpp.sh 2>&1 | tee build/cpp_build.log
CPP_RESULT=${PIPESTATUS[0]}

# Build Go component
echo ""
echo "2. Building Go Quantum API..."
./scripts/build_go.sh 2>&1 | tee build/go_build.log
GO_RESULT=${PIPESTATUS[0]}

# Build Java component
echo ""
echo "3. Building Java Quantum Service..."
./scripts/build_java.sh 2>&1 | tee build/java_build.log
JAVA_RESULT=${PIPESTATUS[0]}

# Build Python virtual environment
echo ""
echo "4. Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt 2>&1 | tee build/python_setup.log
PYTHON_RESULT=${PIPESTATUS[0]}

# Build Node.js dependencies
echo ""
echo "5. Installing Node.js dependencies..."
cd src/node
npm install 2>&1 | tee ../../build/node_setup.log
NODE_RESULT=${PIPESTATUS[0]}
cd ../..

# Summary
echo ""
echo "=== Build Summary ==="
echo "C++ Build: $(if [ $CPP_RESULT -eq 0 ]; then echo "✓ Success"; else echo "✗ Failed"; fi)"
echo "Go Build: $(if [ $GO_RESULT -eq 0 ]; then echo "✓ Success"; else echo "✗ Failed"; fi)"
echo "Java Build: $(if [ $JAVA_RESULT -eq 0 ]; then echo "✓ Success"; else echo "✗ Failed"; fi)"
echo "Python Setup: $(if [ $PYTHON_RESULT -eq 0 ]; then echo "✓ Success"; else echo "✗ Failed"; fi)"
echo "Node.js Setup: $(if [ $NODE_RESULT -eq 0 ]; then echo "✓ Success"; else echo "✗ Failed"; fi)"

echo ""
echo "Build artifacts are in the 'build' directory."
echo "Log files are in 'build/*.log'"
echo ""
echo "To run all services:"
echo "  make run"
