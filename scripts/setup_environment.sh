#!/bin/bash

echo "=== Quantum JV Platform Environment Setup ==="
echo "Timestamp: $(date)"
echo ""

# Create Python virtual environment
echo "1. Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core Python packages
echo "2. Installing core Python packages..."
pip install numpy scipy pandas matplotlib seaborn
pip install jupyter notebook ipython
pip install scikit-learn tensorflow torch
pip install qiskit pennylane cirq-quil
pip install flask fastapi uvicorn
pip install requests beautifulsoup4 selenium
pip install pytest pylint black flake8

# Install quantum-specific packages
echo "3. Installing quantum computing packages..."
pip install qiskit-ibm-runtime
pip install qiskit-aer
pip install qiskit-machine-learning
pip install tensorflow-quantum
pip install pyquil
pip install amazon-braket-sdk

# Install Node.js packages globally
echo "4. Installing Node.js global packages..."
npm install -g create-react-app
npm install -g next
npm install -g vite
npm install -g typescript
npm install -g nodemon
npm install -g express-generator

# Install Go if not present
if ! command -v go &> /dev/null; then
    echo "5. Installing Go..."
    wget https://go.dev/dl/go1.23.3.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    rm go1.23.3.linux-amd64.tar.gz
fi

# Install Rust if not present
if ! command -v rustc &> /dev/null; then
    echo "6. Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi

# Create requirements.txt
echo "7. Creating requirements files..."
pip freeze > requirements.txt
npm list -g --depth=0 > npm_global_packages.txt

# Create environment configuration
echo "8. Creating environment configuration..."
cat > config/envs/development.env << 'ENV_CONFIG'
# Development Environment Configuration
QUANTUM_BACKEND=simulator
PYTHONPATH=/home/rrmr/quantum-jv-platform/src/python
NODE_ENV=development
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
GO_PATH=/usr/local/go
RUST_PATH=$HOME/.cargo/bin

# API Keys (replace with actual keys)
IBM_QUANTUM_TOKEN=your_ibm_token_here
GOOGLE_QUANTUM_TOKEN=your_google_token_here
AWS_ACCESS_KEY=your_aws_key_here
AWS_SECRET_KEY=your_aws_secret_here

# Application Settings
DEBUG=true
LOG_LEVEL=DEBUG
PORT=8000
QUANTUM_SIMULATOR=qasm_simulator
ENV_CONFIG

echo ""
echo "=== Environment Setup Complete ==="
echo "Virtual environment: venv/"
echo "Python packages: requirements.txt"
echo "Node.js packages: npm_global_packages.txt"
echo "Environment config: config/envs/development.env"
echo ""
echo "To activate virtual environment: source venv/bin/activate"
echo "To deactivate: deactivate"
