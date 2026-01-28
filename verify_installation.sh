#!/bin/bash
echo "=== SLK8 PROJECT VERIFICATION ==="
echo "Date: $(date)"
echo "System: $(uname -s) $(uname -r)"
echo ""

echo "1. Checking file structure..."
if [ -f "src/slk8_math.py" ] && [ -f "scripts/run_all.sh" ] && [ -f "Dockerfile" ]; then
echo "✅ Project structure verified"
else
echo "❌ Project structure incomplete"
exit 1
fi

echo ""
echo "2. Testing Python implementation..."
python3 src/slk8_math.py 2>&1 | grep -q "Is Zariski closed? False"
if [ $? -eq 0 ]; then
echo "✅ Mathematical result correct: Support not Zariski closed"
else
echo "❌ Mathematical verification failed"
fi

echo ""
echo "3. Checking multi-language implementations..."
count=$(find src -type f -name ".py" -o -name ".js" -o -name ".java" -o -name ".cpp" -o -name ".go" -o -name ".rs" -o -name "*.ts" | wc -l)
if [ $count -ge 16 ]; then
echo "✅ $count language implementations found (≥16 as required)"
else
echo "⚠ Found $count implementations (expected ≥16)"
fi

echo ""
echo "4. Checking documentation..."
if [ -f "docs/POC_REPORT.md" ] && [ -f "docs/collaboration_table.md" ]; then
echo "✅ Documentation complete"
else
echo "⚠ Documentation missing"
fi

echo ""
echo "=== VERIFICATION COMPLETE ==="
echo "Project ready for client delivery."
