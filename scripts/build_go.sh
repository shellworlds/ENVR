#!/bin/bash

echo "=== Building Go Quantum API ==="

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo "Go not found. Installing..."
    
    if [ -f /etc/debian_version ]; then
        sudo apt update
        sudo apt install -y golang-go
    elif [ "$(uname)" == "Darwin" ]; then
        brew install go
    else
        echo "Please install Go manually from: https://go.dev/dl/"
        exit 1
    fi
fi

# Create Go module if not exists
if [ ! -f src/go/go.mod ]; then
    cd src/go
    go mod init quantum-jv-platform
    cd ../..
fi

# Build Go application
cd src/go
echo "Building Go quantum API..."
go build -o ../../build/go/quantum_api quantum_api.go

if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "Binary created: build/go/quantum_api"
    
    # Create sample run command
    echo ""
    echo "To run the Go quantum API:"
    echo "  cd build/go"
    echo "  ./quantum_api"
    echo ""
    echo "API will be available at: http://localhost:8080"
else
    echo "Build failed!"
    exit 1
fi
