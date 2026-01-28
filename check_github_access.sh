#!/bin/bash
echo "=== GITHUB ACCESS DIAGNOSTIC ==="
echo ""

echo "1. SSH Authentication:"
ssh -T git@github.com 2>&1 | grep -i "successfully authenticated" && echo "✅ SSH working" || echo "❌ SSH issue"

echo ""
echo "2. Repository Existence:"
REPO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://github.com/shellworlds/ENVR")
echo "   HTTP Status: $REPO_STATUS"
if [ "$REPO_STATUS" = "200" ]; then
    echo "   ✅ Repository exists"
elif [ "$REPO_STATUS" = "404" ]; then
    echo "   ❌ Repository not found"
    echo "   Create it at: https://github.com/new"
else
    echo "   ⚠ Unexpected status"
fi

echo ""
echo "3. Current Directory Git Status:"
cd ~/SLK8-Project
git remote -v
echo "Current branch: $(git branch --show-current)"

echo ""
echo "=== QUICK FIXES ==="
echo "If repository doesn't exist:"
echo "  Create at: https://github.com/new"
echo "  Name: ENVR"
echo "  Public repository"
echo "  Don't initialize with README"
echo ""
echo "After creating repository:"
echo "  git remote remove origin"
echo "  git remote add origin git@github.com:shellworlds/ENVR.git"
echo "  git push origin ENVR48"
