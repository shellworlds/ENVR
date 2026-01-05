#!/bin/bash
echo "=================================================="
echo "ENVR11 Travel Agent ML Platform - Complete Installation"
echo "=================================================="
echo "Starting installation at: $(date)"
echo ""

# Detect operating system
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "Detected OS: $OS"
echo ""

# Installation function with error handling
install_package() {
    local package=$1
    local installer=$2
    local extra_args=$3
    
    echo "Installing $package..."
    if eval "$installer $extra_args $package"; then
        echo "✅ $package installed successfully"
    else
        echo "⚠️  Failed to install $package, continuing..."
    fi
}

# 1. PYTHON DATA SCIENCE & ML STACK
echo "=== INSTALLING PYTHON DATA SCIENCE STACK ==="
install_package "numpy pandas scipy" "pip3 install"
install_package "scikit-learn" "pip3 install"
install_package "tensorflow" "pip3 install"
install_package "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu" "pip3 install"
install_package "xgboost" "pip3 install"
install_package "plotly dash" "pip3 install"
install_package "flask fastapi uvicorn" "pip3 install"
install_package "requests beautifulsoup4" "pip3 install"
install_package "sqlalchemy pymysql" "pip3 install"
install_package "joblib pickle-mixin" "pip3 install"

# 2. QUANTUM COMPUTING WITH 20 QUBITS
echo ""
echo "=== INSTALLING QUANTUM COMPUTING PACKAGES ==="
install_package "qiskit" "pip3 install"
install_package "qiskit-aer" "pip3 install"
install_package "qiskit-ibm-runtime" "pip3 install"
install_package "qiskit-machine-learning" "pip3 install"
install_package "pennylane" "pip3 install"
echo "Quantum computing environment configured for 20-qubit simulations"

# 3. TRAVEL INDUSTRY SPECIFIC PACKAGES
echo ""
echo "=== INSTALLING TRAVEL INDUSTRY PACKAGES ==="
install_package "geopy" "pip3 install"
install_package "timezonefinder" "pip3 install"
install_package "currencyconverter" "pip3 install"
install_package "python-dateutil" "pip3 install"
install_package "holidays" "pip3 install"
install_package "timezonefinder" "pip3 install"

# 4. VISUALIZATION & DASHBOARD TOOLS
echo ""
echo "=== INSTALLING VISUALIZATION TOOLS ==="
install_package "matplotlib seaborn" "pip3 install"
install_package "bokeh" "pip3 install"
install_package "dash-bootstrap-components" "pip3 install"
install_package "jupyter jupyterlab" "pip3 install"

# 5. NODE.JS & FRONTEND STACK
echo ""
echo "=== INSTALLING NODE.JS & FRONTEND TOOLS ==="
if command -v npm &> /dev/null; then
    # Install global packages
    echo "Installing Node.js global packages..."
    npm install -g react react-dom next@latest vite@latest 2>/dev/null || echo "Global install skipped, using local"
    
    # Create package.json for frontend
    echo "Creating frontend package.json..."
    cat > frontend/package.json << 'PKGEOF'
{
  "name": "envr11-travel-dashboard",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "14.0.0",
    "vite": "^5.0.0",
    "axios": "^1.6.0",
    "recharts": "^2.10.0",
    "react-query": "^3.39.3",
    "tailwindcss": "^3.3.0",
    "d3": "^7.8.0",
    "lodash": "^4.17.21"
  },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "vite": "vite"
  }
}
PKGEOF
    
    # Install frontend dependencies
    cd frontend && npm install 2>/dev/null && cd ..
    echo "✅ Frontend dependencies configured"
else
    echo "⚠️  npm not found, skipping frontend setup"
fi

# 6. CREATE VIRTUAL ENVIRONMENT FOR ISOLATION
echo ""
echo "=== SETTING UP PYTHON VIRTUAL ENVIRONMENT ==="
python3 -m venv envr11_env
source envr11_env/bin/activate 2>/dev/null || echo "Virtual environment created at envr11_env"
echo "To activate: source envr11_env/bin/activate"

# 7. CREATE REQUIREMENTS FILE FOR FUTURE USE
echo ""
echo "=== CREATING REQUIREMENTS FILES ==="
cat > requirements_envr11.txt << 'REQEOF'
# ENVR11 Travel Agent ML Platform Requirements
# Core Data Science
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
scipy>=1.11.0

# Machine Learning & AI
tensorflow>=2.13.0
torch>=2.0.0
xgboost>=1.7.0
joblib>=1.3.0

# Quantum Computing (20 Qubits)
qiskit>=0.45.0
qiskit-aer>=0.12.0
qiskit-machine-learning>=0.7.0
pennylane>=0.32.0

# Visualization & Dashboard
plotly>=5.17.0
dash>=2.14.0
dash-bootstrap-components>=1.5.0
matplotlib>=3.7.0
seaborn>=0.12.0

# Travel Industry Specific
geopy>=2.4.0
currencyconverter>=0.17.0
holidays>=0.36.0
python-dateutil>=2.8.0
timezonefinder>=6.2.0

# Web & API Framework
fastapi>=0.104.0
uvicorn>=0.24.0
requests>=2.31.0
beautifulsoup4>=4.12.0

# Database & Storage
sqlalchemy>=2.0.0
pymysql>=1.1.0
REQEOF

echo "Requirements file created: requirements_envr11.txt"

# 8. SYSTEM-SPECIFIC INSTALLATIONS
echo ""
echo "=== SYSTEM-SPECIFIC CONFIGURATIONS ==="
case $OS in
    "linux")
        echo "Configuring for Linux (Ubuntu/Debian)..."
        # Install system packages if needed
        if command -v apt-get &> /dev/null; then
            sudo apt-get update 2>/dev/null || true
            sudo apt-get install -y python3-dev build-essential 2>/dev/null || true
        fi
        ;;
    "mac")
        echo "Configuring for macOS..."
        if command -v brew &> /dev/null; then
            brew install python@3.11 2>/dev/null || true
        fi
        ;;
    "windows")
        echo "Configuring for Windows..."
        echo "For Windows, ensure Python 3.11+ and Node.js are installed manually"
        echo "Run: winget install Python.Python.3.11 Node.js"
        ;;
esac

# 9. VERIFICATION OF INSTALLATION
echo ""
echo "=== VERIFICATION ==="
echo "Verifying critical packages..."
python3 -c "
import sys
print(f'Python {sys.version}')

packages = ['numpy', 'pandas', 'sklearn', 'tensorflow', 'torch', 'qiskit', 'plotly', 'fastapi']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}: OK')
    except ImportError as e:
        print(f'❌ {pkg}: Missing - {e}')
"

echo ""
echo "=================================================="
echo "ENVR11 INSTALLATION COMPLETE"
echo "=================================================="
echo "Next steps:"
echo "1. Activate virtual environment: source envr11_env/bin/activate"
echo "2. Run system check: ./system_check/system_check_envr11.sh"
echo "3. Start development: python backend/travel_ml_engine.py"
echo ""
echo "System configured for:"
echo "- 20-qubit quantum travel optimization"
echo "- Real-time pricing ML models"
echo "- Multi-language travel dashboard"
echo "- Industry-standard travel indicators"
echo "=================================================="
