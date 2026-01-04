#!/bin/bash
echo "ENVR9 SYSTEM CHECK INITIATED"
echo "Timestamp: $(date)"
echo "1. OPERATING SYSTEM:"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux detected"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Windows detected"
else
    echo "Unknown OS: $OSTYPE"
fi
echo "2. SYSTEM ARCHITECTURE AND DETAILS:"
ARCH=$(uname -m)
echo "Architecture: $ARCH"
echo "Kernel Version: $(uname -r)"
echo "Hostname: $(hostname)"
echo "CPU Cores: $(nproc)"
echo "3. PYTHON ENVIRONMENT:"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "Python $PYTHON_VERSION available"
    echo "Python Path: $(which python3)"
else
    echo "Python3 not found"
fi
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    echo "pip $PIP_VERSION available"
else
    echo "pip3 not found"
fi
echo "4. NODE.JS ENVIRONMENT:"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "Node.js $NODE_VERSION available"
    echo "Node Path: $(which node)"
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        echo "npm $NPM_VERSION available"
    else
        echo "npm not found"
    fi
else
    echo "Node.js not found"
fi
echo "5. JAVA ENVIRONMENT:"
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
    echo "Java $JAVA_VERSION available"
    echo "Java Path: $(which java)"
else
    echo "Java not found"
fi
echo "6. GIT ENVIRONMENT:"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo "Git $GIT_VERSION available"
    echo "Git Path: $(which git)"
else
    echo "Git not found"
fi
echo "7. DOCKER ENVIRONMENT:"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    echo "Docker $DOCKER_VERSION available"
    docker info --format 'Docker Root Dir: {{.DockerRootDir}}' 2>/dev/null | head -1
else
    echo "Docker not found"
fi
echo "8. SYSTEM RESOURCES:"
echo "Memory:"
free -h | awk '/^Mem:/ {print "  Total: "$2", Available: "$7}'
echo "Disk Space:"
df -h . | tail -1 | awk '{print "  Available: "$4" on "$1}'
echo "Uptime: $(uptime -p)"
