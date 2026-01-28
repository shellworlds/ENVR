#!/bin/bash
# SLK8 Project Installation Script
# Works on Linux, Mac, and Windows (via WSL)

set -e

echo "=== SLK8 Project Installation ==="
echo "Support Analysis of M = Q/Z Module"
echo ""

# Detect OS
case "$(uname -s)" in
    Linux*)     OS="Linux" ;;
    Darwin*)    OS="Mac" ;;
    CYGWIN*|MINGW*|MSYS*) OS="Windows" ;;
    *)          OS="Unknown" ;;
esac

echo "Detected OS: $OS"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Git
if command -v git >/dev/null 2>&1; then
    echo "✓ Git: $(git --version)"
else
    echo "✗ Git not found. Please install Git first."
    if [ "$OS" = "Linux" ]; then
        echo "  Ubuntu/Debian: sudo apt-get install git"
        echo "  RHEL/Fedora: sudo yum install git"
    elif [ "$OS" = "Mac" ]; then
        echo "  brew install git"
    elif [ "$OS" = "Windows" ]; then
        echo "  Download from: https://git-scm.com/download/win"
    fi
    exit 1
fi

# Python
if command -v python3 >/dev/null 2>&1; then
    echo "✓ Python: $(python3 --version)"
else
    echo "✗ Python3 not found. Installing..."
    if [ "$OS" = "Linux" ]; then
        sudo apt-get install python3 python3-pip -y
    elif [ "$OS" = "Mac" ]; then
        brew install python3
    elif [ "$OS" = "Windows" ]; then
        echo "Please install Python from: https://www.python.org/downloads/"
        exit 1
    fi
fi

# Node.js (optional)
if command -v node >/dev/null 2>&1; then
    echo "✓ Node.js: $(node --version)"
    echo "✓ npm: $(npm --version)"
else
    echo "⚠ Node.js not found (optional for web features)"
fi

# Clone or update project
echo ""
echo "Setting up project..."

if [ -d "SLK8-Project" ]; then
    echo "Project exists, updating..."
    cd SLK8-Project
    git pull origin main
else
    echo "Cloning project..."
    git clone https://github.com/shellworlds/ENVR.git SLK8-Project
    cd SLK8-Project
    git checkout ENVR48 2>/dev/null || true
fi

# Install dependencies
echo ""
echo "Installing dependencies..."

# Python dependencies
echo "Installing Python packages..."
python3 -m pip install --upgrade pip
python3 -m pip install sympy numpy matplotlib pytest

# Node.js dependencies (if available)
if command -v npm >/dev/null 2>&1; then
    echo "Installing Node.js packages..."
    npm install
fi

# Set up execution permissions
chmod +x scripts/*.sh

echo ""
echo "=== INSTALLATION COMPLETE ==="
echo ""
echo "To run the project:"
echo "  cd SLK8-Project"
echo "  ./scripts/run_all.sh"
echo ""
echo "Or run individual implementations:"
echo "  python3 src/slk8_math.py        # Python"
echo "  node src/slk8.js                # JavaScript"
echo "  ./scripts/setup.sh              # System setup"
echo ""
echo "For web dashboard:"
echo "  Open src/dashboard.html in browser"
echo ""
echo "Mathematical Result:"
echo "  Support(M = ℚ/ℤ) = { (p) | p prime }"
echo "  Not Zariski closed in Spec(ℤ)"
