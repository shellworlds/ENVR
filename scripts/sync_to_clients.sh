#!/bin/bash

echo "=== Syncing Quantum JV Platform to Client Repositories ==="
echo "Timestamp: $(date)"
echo ""

# Create clients directory if it doesn't exist
mkdir -p clients

# Files to sync
SYNC_FILES=(
    "src/python/quantum_base.py"
    "src/python/clients/"
    "src/react/QuantumComponent.jsx"
    "src/react/QuantumComponent.css"
    "src/node/server.js"
    "src/node/package.json"
    "src/cpp/quantum_simulator.cpp"
    "src/go/quantum_api.go"
    "src/java/QuantumService.java"
    "README.md"
    "Makefile"
    ".github/workflows/quantum-ci.yml"
    "scripts/"
    "docs/"
    "config/"
)

# Client directories
CLIENT_DIRS=("clients/ZENVR" "clients/DENVR" "clients/QENVR" "clients/AENVR" "clients/BENVR" "clients/ENVR")

for client_dir in "${CLIENT_DIRS[@]}"; do
    client=$(basename "$client_dir")
    
    echo "Processing: $client"
    echo "Directory: $client_dir"
    
    # Create client directory structure
    mkdir -p "${client_dir}/src/python"
    mkdir -p "${client_dir}/src/python/clients"
    mkdir -p "${client_dir}/src/react"
    mkdir -p "${client_dir}/src/node"
    mkdir -p "${client_dir}/src/cpp"
    mkdir -p "${client_dir}/src/go"
    mkdir -p "${client_dir}/src/java"
    mkdir -p "${client_dir}/scripts"
    mkdir -p "${client_dir}/docs"
    mkdir -p "${client_dir}/config"
    mkdir -p "${client_dir}/.github/workflows"
    
    # Copy files
    for file in "${SYNC_FILES[@]}"; do
        if [ -e "$file" ]; then
            if [ -d "$file" ]; then
                cp -r "$file" "${client_dir}/$(dirname "$file")/" 2>/dev/null || true
            else
                cp "$file" "${client_dir}/$(dirname "$file")/" 2>/dev/null || true
            fi
            echo "  ✓ $file"
        fi
    done
    
    # Create client-specific README
    cat > "${client_dir}/README.md" << CLIENT_README
# $client - Quantum JV Platform Integration

## Client Information
- **Client**: $client
- **Integration Date**: $(date)
- **Platform Version**: 1.0.0

## Quantum Modules Included
1. **Python Quantum Base** - Core quantum operations
2. **C++ Quantum Simulator** - High-performance simulation
3. **Go Quantum API** - REST API server
4. **Java Quantum Service** - Enterprise service
5. **React Quantum Component** - Visualization
6. **Node.js Server** - API endpoints

## Quick Start
\`\`\`bash
# Build all components
./scripts/build_all.sh

# Run Python quantum examples
python src/python/quantum_base.py

# Run C++ simulator
./scripts/build_cpp.sh

# Start Node.js server
cd src/node && npm start
\`\`\`

## API Documentation
- Health check: \`GET /api/quantum/health\`
- Quantum simulation: \`POST /api/quantum/simulate\`
- Circuit creation: \`POST /api/quantum/circuit\`

## Support
For quantum platform support, contact: quantum-support@shellworlds.com
CLIENT_README
    
    echo "  Created client-specific README"
    echo ""
done

echo "=== Sync Complete ==="
echo ""
echo "Files have been synchronized to client directories."
echo "Client directories created:"
ls -la clients/
