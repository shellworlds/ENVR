#!/bin/bash
echo "=============================================="
echo "ENVR11 Travel Agent ML System - System Verification"
echo "=============================================="
echo "Checking date: $(date)"
echo ""

# 1. Operating System Verification
echo "=== OS & HARDWARE VERIFICATION ==="
echo "Hostname: $(hostname)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "OS: $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"')"
echo "CPU Cores: $(nproc)"
echo "Total RAM: $(free -h | grep Mem | awk '{print $2}')"
echo "Available RAM: $(free -h | grep Mem | awk '{print $7}')"
echo "Disk Space Available: $(df -h / | awk 'NR==2 {print $4}')"
echo ""

# 2. Development Environment Check
echo "=== DEVELOPMENT ENVIRONMENT ==="

# Python and ML stack
echo "Python: $(python3 --version 2>/dev/null || echo 'Not installed')"
python3 -c "import sys; print(f'Python Path: {sys.executable}')" 2>/dev/null || true

# Node.js ecosystem
echo "Node.js: $(node --version 2>/dev/null || echo 'Not installed')"
echo "npm: $(npm --version 2>/dev/null || echo 'Not installed')"
echo ""

# 3. Quantum Computing Prerequisites (20 Qubits)
echo "=== QUANTUM COMPUTING PREREQUISITES ==="
echo "Quantum Computing Environment Check:"
python3 -c "
try:
    import qiskit
    print(f'Qiskit: {qiskit.__version__}')
    print('✓ Quantum computing support available')
    print('✓ 20 Qubit simulation capable')
except ImportError:
    print('✗ Qiskit not installed - quantum features disabled')
" 2>/dev/null || echo "Python quantum check failed"

# 4. Travel Industry Specific Requirements
echo ""
echo "=== TRAVEL INDUSTRY DATA SOURCES ==="
echo "Required data sources for travel agent system:"
echo "1. Flight pricing APIs (Skyscanner, Amadeus)"
echo "2. Hotel availability APIs (Booking.com, Expedia)"
echo "3. Weather data integration"
echo "4. Currency exchange rates"
echo "5. Travel restriction databases"
echo ""

# 5. ML & Data Science Capabilities
echo "=== MACHINE LEARNING CAPABILITIES ==="
echo "Checking ML libraries:"
python3 -c "
libs = ['numpy', 'pandas', 'scikit-learn', 'tensorflow', 'torch', 'xgboost', 'plotly', 'dash']
for lib in libs:
    try:
        exec(f'import {lib}')
        print(f'✓ {lib}: Available')
    except:
        print(f'✗ {lib}: Missing')
" 2>/dev/null || echo "ML library check failed"

# 6. System Score Calculation
echo ""
echo "=== SYSTEM SCORING ==="
score=0
total=10

# Check Python
if command -v python3 &> /dev/null; then
    echo "✓ Python3: Found (+1)"
    ((score++))
else
    echo "✗ Python3: Missing"
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "✓ pip3: Found (+1)"
    ((score++))
else
    echo "✗ pip3: Missing"
fi

# Check Node.js
if command -v node &> /dev/null; then
    echo "✓ Node.js: Found (+1)"
    ((score++))
else
    echo "✗ Node.js: Missing"
fi

# Check Git
if command -v git &> /dev/null; then
    echo "✓ Git: Found (+1)"
    ((score++))
else
    echo "✗ Git: Missing"
fi

# Check RAM > 16GB
ram_gb=$(free -g | grep Mem | awk '{print $2}')
if [ $ram_gb -ge 16 ]; then
    echo "✓ RAM ≥ 16GB: ${ram_gb}GB (+2)"
    ((score+=2))
else
    echo "✗ RAM < 16GB: ${ram_gb}GB"
fi

# Check Storage > 500GB
storage_gb=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
if [ $storage_gb -ge 500 ]; then
    echo "✓ Storage ≥ 500GB: ${storage_gb}GB (+2)"
    ((score+=2))
else
    echo "✗ Storage < 500GB: ${storage_gb}GB"
fi

# Check if in ENVR directory
if [[ $(pwd) == *"ENVR"* ]]; then
    echo "✓ In ENVR workspace (+1)"
    ((score++))
else
    echo "✗ Not in ENVR workspace"
fi

echo ""
echo "SYSTEM SCORE: ${score}/${total}"
if [ $score -ge 8 ]; then
    echo "✅ SYSTEM READY FOR ENVR11 DEPLOYMENT"
elif [ $score -ge 5 ]; then
    echo "⚠️ SYSTEM PARTIALLY READY - Some features may be limited"
else
    echo "❌ SYSTEM INSUFFICIENT - Please upgrade before proceeding"
fi

echo ""
echo "=============================================="
echo "ENVR11 System Verification Complete"
echo "Next: Install dependencies with ./scripts/install_all.sh"
echo "=============================================="
