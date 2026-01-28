#!/bin/bash
# Script to setup all client repositories

set -e  # Exit on error

REPO_BASE="git@github.com:"
REPOS=(
    "Zius-Global/ZENVR"
    "dt-uk/DENVR" 
    "qb-eu/QENVR"
    "vipul-zius/ZENVR"
    "mike-aeq/AENVR"
    "shellworlds/ZENVR"
    "shellworlds/DENVR"
    "shellworlds/QENVR"
    "shellworlds/AENVR"
    "shellworlds/ENVR"
)

echo "Setting up client repositories..."

# Create repositories directory
mkdir -p ../envr-client-repos
cd ../envr-client-repos

for repo in "${REPOS[@]}"; do
    # Extract repo name (last part after /)
    repo_name=$(basename "$repo")
    echo "Processing $repo..."
    
    # Clone if not exists
    if [ ! -d "$repo_name" ]; then
        git clone "${REPO_BASE}${repo}.git" "$repo_name" || echo "Clone failed for $repo - may need access"
    fi
    
    # Navigate to repo
    if [ -d "$repo_name" ]; then
        cd "$repo_name"
        
        # Create new branch based on repo name
        branch_name="${repo_name}41"
        git checkout -b "$branch_name" 2>/dev/null || git checkout "$branch_name"
        
        # Return to parent
        cd ..
    fi
done

echo "Repository setup complete in: $(pwd)"
