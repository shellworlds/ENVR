#!/bin/bash
# ENVR Quantum Computing Environment Setup
# For Lenovo ThinkPad with Ubuntu/Linux

set -e  # Exit on error

echo "========================================="
echo "ENVR Quantum Computing Environment Setup"
echo "========================================="

# Check Python
echo "✓ Checking Python..."
python3 --version || { echo "Python3 not found"; exit 1; }

# Create and activate venv
echo "✓ Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install packages
echo "✓ Installing packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup pre-commit
echo "✓ Setting up pre-commit..."
pip install pre-commit
pre-commit install

# Test Qiskit
echo "✓ Testing Qiskit..."
python3 -c "import qiskit; print(f'Qiskit {qiskit.__version__} installed')"

# Simple quantum test
echo "✓ Running quantum test..."
python3 -c "
from qiskit import QuantumCircuit, Aer, execute
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()
result = execute(qc, Aer.get_backend('qasm_simulator')).result()
print('Quantum simulation successful')
"

echo "========================================="
echo "✅ SETUP COMPLETE!"
echo "========================================="
echo "Virtual environment: venv/"
echo "Activate: source venv/bin/activate"
echo "Test: python -m pytest tests/"
echo "Pre-commit: pre-commit run --all-files"
echo "========================================="
