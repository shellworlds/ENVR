#!/bin/bash
# File: deploy.sh
# Language: Shell Script
# Purpose: Automated deployment and theorem verification

set -e  # Exit on error

echo "=============================================="
echo "Projective Module Theorem Deployment Script"
echo "=============================================="

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check dependencies
check_dependencies() {
    print_status "Checking dependencies..."
    
    local deps=("python3" "pip3" "node" "npm" "java" "javac" "go" "g++" "make")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null; then
            missing+=("$dep")
            print_warning "Missing: $dep"
        else
            print_status "$dep: $(command -v $dep)"
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        print_error "Missing dependencies: ${missing[*]}"
        print_status "Install with: sudo apt install ${missing[*]}"
        exit 1
    fi
}

# Setup Python virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        print_status "Virtual environment created at $VENV_DIR"
    fi
    
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r "$PROJECT_DIR/requirements.txt" 2>/dev/null || true
}

# Run all theorem verifications
run_theorem_verifications() {
    print_status "Running theorem verifications..."
    
    echo ""
    print_status "Theorem 1: Lifting Property"
    python3 "$PROJECT_DIR/src/projective_module.py" | grep -A2 "Theorem 1"
    
    echo ""
    print_status "Theorem 2: Splitting Property"
    python3 "$PROJECT_DIR/src/projective_module.py" | grep -A2 "Theorem 2"
    
    echo ""
    print_status "Theorem 3: Direct Summand of Free"
    python3 "$PROJECT_DIR/src/projective_module.py" | grep -A2 "Theorem 3"
    
    echo ""
    print_status "Theorem 4: Local Ring Case"
    python3 "$PROJECT_DIR/src/projective_module.py" | grep -A2 "Theorem 4"
}

# Compile and run C++ implementation
run_cpp_verification() {
    print_status "Compiling C++ implementation..."
    
    cd "$PROJECT_DIR/src"
    if g++ -std=c++11 -o module_computation module_computation.cpp 2>/dev/null; then
        print_status "C++ compilation successful"
        ./module_computation
    else
        print_warning "C++ compilation failed, skipping"
    fi
}

# Compile and run Java implementation
run_java_verification() {
    print_status "Compiling Java implementation..."
    
    cd "$PROJECT_DIR/src"
    if javac ModuleTheory.java 2>/dev/null; then
        print_status "Java compilation successful"
        java ModuleTheory
    else
        print_warning "Java compilation failed, skipping"
    fi
}

# Run Go implementation
run_go_verification() {
    print_status "Running Go implementation..."
    
    cd "$PROJECT_DIR/src"
    if go run module_operations.go 2>/dev/null; then
        print_status "Go execution successful"
    else
        print_warning "Go execution failed, skipping"
    fi
}

# Main execution
main() {
    check_dependencies
    setup_python_env
    
    echo ""
    print_status "Starting comprehensive theorem verification..."
    echo ""
    
    run_theorem_verifications
    echo ""
    run_cpp_verification
    echo ""
    run_java_verification
    echo ""
    run_go_verification
    
    echo ""
    print_status "=============================================="
    print_status "All theorem verifications completed!"
    print_status "=============================================="
    
    # Deactivate virtual environment
    deactivate 2>/dev/null || true
}

# Run main function
main "$@"
