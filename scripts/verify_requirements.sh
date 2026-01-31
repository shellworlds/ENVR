#!/bin/bash

echo "=== Quantum JV Platform Requirements Verification ==="
echo "Timestamp: $(date)"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_command() {
    local cmd=$1
    local version_flag=$2
    
    if command -v $cmd &> /dev/null; then
        version=$($cmd $version_flag 2>&1 | head -1)
        echo -e "${GREEN}✓${NC} $cmd: $version"
        return 0
    else
        echo -e "${RED}✗${NC} $cmd: NOT FOUND"
        return 1
    fi
}

echo "1. Core System Information:"
echo "   OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"')"
echo "   Kernel: $(uname -r)"
echo "   Architecture: $(uname -m)"
echo ""

echo "2. Required Tools:"
check_command "python3" "--version"
check_command "pip3" "--version"
check_command "node" "--version"
check_command "npm" "--version"
check_command "java" "-version"
check_command "git" "--version"
echo ""

echo "3. Disk Space Check:"
df -h /home | tail -1 | awk '{print "   Available: "$4" / "$2}'
echo ""

echo "4. RAM Availability:"
free -h | grep Mem | awk '{print "   Total: "$2", Available: "$7}'
echo ""

echo "5. GitHub SSH Authentication:"
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo -e "${GREEN}✓ GitHub SSH authentication successful${NC}"
    ssh -T git@github.com 2>&1 | head -1
else
    echo -e "${RED}✗ GitHub SSH authentication failed${NC}"
fi
echo ""

echo "6. Network Connectivity:"
if ping -c 1 github.com &> /dev/null; then
    echo -e "${GREEN}✓ Network connectivity OK${NC}"
else
    echo -e "${RED}✗ Network connectivity issue${NC}"
fi
echo ""

echo "=== Verification Complete ==="
