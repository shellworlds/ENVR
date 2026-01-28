#!/bin/bash
echo "Verifying GitHub repositories..."
echo ""

# Test main repository
echo "1. Testing shellworlds/ENVR:"
if curl -s "https://api.github.com/repos/shellworlds/ENVR/branches/ENVR48" | grep -q "not found"; then
    echo "   ⚠ ENVR48 branch not found on remote"
    echo "   To create: git push origin ENVR48"
else
    echo "   ✅ ENVR48 branch exists"
fi

echo ""
echo "2. Testing other client repositories:"
repos=("Zius-Global/ZENVR" "dt-uk/DENVR" "qb-eu/QENVR" "mike-aeq/AENVR" "manav2341/BENVR")
for repo in "${repos[@]}"; do
    branch="${repo##*/}48"
    echo "   $repo/$branch: https://github.com/$repo/tree/$branch"
done

echo ""
echo "3. Quick access commands:"
echo "   To view ENVR48: https://github.com/shellworlds/ENVR/tree/ENVR48"
echo "   To clone: git clone https://github.com/shellworlds/ENVR.git --branch ENVR48"
echo "   To push if missing: git push origin ENVR48"
