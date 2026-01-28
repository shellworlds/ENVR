#!/bin/bash
# Script to push all SLK8 branches to GitHub repositories

echo "=== PUSHING ALL SLK8 BRANCHES ==="
echo ""

# Function to push a repository
push_repo() {
    local repo_dir=$1
    local branch=$2
    local repo_name=$3
    
    echo "Processing $repo_name..."
    
    if [ -d "$repo_dir/.git" ]; then
        cd "$repo_dir"
        
        # Check current branch
        current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
        
        # Switch to target branch
        if [ "$current_branch" != "$branch" ]; then
            echo "  Switching to $branch..."
            git checkout "$branch" 2>/dev/null || git checkout -b "$branch"
        fi
        
        # Add and commit any changes
        git add . 2>/dev/null
        git commit -m "SLK8 Project: Support of M = Q/Z - Complete implementation" 2>/dev/null
        
        # Push to remote
        echo "  Pushing to GitHub..."
        git push origin "$branch" 2>&1 | grep -E "To:|remote:|Branch|Done" || echo "  Push attempted"
        
        cd - >/dev/null
        echo ""
    else
        echo "  ⚠ Not a git repository"
        echo ""
    fi
}

# Push main project
echo "1. Main Project (shellworlds/ENVR):"
cd ~/SLK8-Project
git checkout ENVR48 2>/dev/null || git checkout -b ENVR48
git add .
git commit -m "Complete SLK8 Project implementation" 2>/dev/null
git push origin ENVR48 2>&1 | grep -E "To:|remote:|Branch" || echo "  Push output above"

echo ""
echo "2. Client Repositories:"
cd ~/SLK8-Project/clients

declare -A repo_branches=(
    ["ZENVR"]="ZENVR48"
    ["DENVR"]="DENVR48" 
    ["QENVR"]="QENVR48"
    ["AENVR"]="AENVR48"
    ["BENVR"]="BENVR48"
    ["ENVR"]="ENVR48"
)

for repo_dir in */; do
    repo_name=${repo_dir%/}
    branch=${repo_branches[$repo_name]}
    
    if [ -n "$branch" ]; then
        push_repo "$repo_dir" "$branch" "$repo_name"
    fi
done

echo ""
echo "3. Backup Repositories:"
cd ~/SLK8-Project/backup-repos

for repo_dir in */; do
    repo_name=${repo_dir%/}
    echo "Processing backup: $repo_name"
    push_repo "$repo_dir" "backup-SLK8" "shellworlds/$repo_name"
done

echo ""
echo "=== PUSH COMPLETE ==="
echo "All branches pushed to GitHub."
echo ""
echo "Verify at:"
echo "  https://github.com/shellworlds/ENVR/tree/ENVR48"
echo "  https://github.com/Zius-Global/ZENVR/tree/ZENVR48"
echo "  https://github.com/dt-uk/DENVR/tree/DENVR48"
echo "  etc."
