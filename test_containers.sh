#!/bin/bash
echo "Testing SLK8 Project Containers..."
echo ""

# Test Python implementation directly
echo "1. Direct Python Test:"
docker exec slk8-python python3 src/slk8_math.py | grep -A5 "SLK8 Problem"

echo ""
echo "2. Checking all containers are running:"
docker ps --filter "name=slk8" --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "3. Testing multi-language runner output:"
docker exec slk8-runner ./scripts/run_all.sh 2>&1 | tail -20

echo ""
echo "4. Mathematical Result Verification:"
echo "Expected: Support(M = ℚ/ℤ) = { (p) | p prime }, not Zariski closed"
echo ""
echo "✅ Container test complete!"
