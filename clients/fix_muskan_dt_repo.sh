#!/bin/bash
# Script to fix muskan-dt/DENVR repository issues

echo "=== FIXING MUSKAN-DT/DENVR ACCESS ==="
echo ""

# Option 1: Use dt-uk/DENVR (recommended)
echo "1. Using dt-uk/DENVR repository:"
echo "   Primary URL: https://github.com/dt-uk/DENVR/tree/DENVR48"
echo "   This is the main organization repository"
echo "   muskan-dt should have collaborator access here"
echo ""

# Option 2: Create a fork or use backup
echo "2. Alternative solutions:"
echo "   a. Fork dt-uk/DENVR to muskan-dt/DENVR"
echo "   b. Use shellworlds/DENVR as collaboration point"
echo "   c. Create new repository under muskan-dt"
echo ""

# Check current access
echo "3. Current access status:"
echo "   - dt-uk/DENVR: Organization repository"
echo "   - muskan-dt: Should be collaborator on dt-uk/DENVR"
echo "   - Email: muskan.s@data-t.space"
echo ""

# Create a collaboration document
cat > MUSKAN-DT_COLLABORATION.md << 'DOC'
# Collaboration Setup for muskan-dt

## Current Status
- Primary repository: dt-uk/DENVR (organization)
- Desired repository: muskan-dt/DENVR (personal)
- Branch needed: DENVR48

## Solutions

### Solution 1: Use dt-uk/DENVR (Recommended)
muskan-dt should have collaborator access to:
https://github.com/dt-uk/DENVR/tree/DENVR48

### Solution 2: Create Fork
1. Go to: https://github.com/dt-uk/DENVR
2. Click "Fork" (top right)
3. Select "muskan-dt" as owner
4. This creates: https://github.com/muskan-dt/DENVR
5. Then create DENVR48 branch

### Solution 3: Use Backup Repository
Access: https://github.com/shellworlds/DENVR/tree/backup-SLK8
Contains complete SLK8 project implementation.

### Solution 4: Create New Repository
1. Visit: https://github.com/new
2. Owner: muskan-dt
3. Name: DENVR
4. Clone from: https://github.com/shellworlds/ENVR.git
5. Checkout ENVR48 branch

## Contact Information
- muskan-dt GitHub: https://github.com/muskan-dt
- Email: muskan.s@data-t.space
- Project: SLK8 Support Analysis

## Verification
To verify access, muskan-dt should be able to:
1. Access https://github.com/dt-uk/DENVR
2. Create/see DENVR48 branch
3. Push changes to the repository

If not, request collaborator access from dt-uk organization admin.
DOC

echo "Collaboration document created: MUSKAN-DT_COLLABORATION.md"
echo ""
echo "=== ACTION REQUIRED ==="
echo "muskan-dt needs to either:"
echo "1. Get collaborator access to dt-uk/DENVR"
echo "2. Fork dt-uk/DENVR to personal account"
echo "3. Use shellworlds/DENVR as backup"
echo ""
echo "Current working URL: https://github.com/dt-uk/DENVR/tree/DENVR48"
