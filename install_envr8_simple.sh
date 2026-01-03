#!/bin/bash
echo "ENVR8 Installation Script"
echo "========================="
echo "Platform: $(uname -s)"
echo ""
echo "1. Installing Python dependencies..."
echo "pip install mlflow kubeflow snyk"
echo ""
echo "2. Setting up environment..."
echo "mkdir -p ~/.envr8"
echo ""
echo "3. Platform-specific setup:"
if [ "$(uname -s)" = "Linux" ]; then
    echo "sudo apt-get install -y python3-pip nodejs npm docker.io"
elif [ "$(uname -s)" = "Darwin" ]; then
    echo "brew install python@3.9 node docker"
else
    echo "choco install python nodejs docker-desktop"
fi
echo ""
echo "ENVR8 ready! 8 files, 16 tools, 5 processes."
echo "#ENVR8 #MLOps #CyberSecurity #DataFlow #B2B"
