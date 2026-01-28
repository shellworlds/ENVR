#!/bin/bash
# Push ENVR Module Splitter to all repositories

set -e

echo "ENVR Module Splitter - Final Push to All Repositories"
echo "====================================================="

# Define all repositories
REPOS=(
    # Primary client repos (write access)
    "Zius-Global/ZENVR:ZENVR41"
    "dt-uk/DENVR:DENVR41"
    "qb-eu/QENVR:QENVR41"
    "vipul-zius/ZENVR:ZENVR41"
    "mike-aeq/AENVR:AENVR41"
    
    # Backup repos (need to exist first)
    "shellworlds/ZENVR:ZENVR41"
    "shellworlds/DENVR:DENVR41"
    "shellworlds/QENVR:QENVR41"
    "shellworlds/AENVR:AENVR41"
    "shellworlds/ENVR:ENVR41"
)

push_to_repo() {
    local repo=$1
    local branch=$2
    
    echo -e "\n📦 Pushing to: $repo (branch: $branch)"
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Clone or create
    git clone "https://github.com/$repo.git" --branch "$branch" 2>/dev/null || \
    git clone "https://github.com/$repo.git" && git checkout -b "$branch"
    
    cd "$(basename "$repo")"
    
    # Copy all files from project
    cp -r ~/envr-module-splitter/* .
    cp -r ~/envr-module-splitter/.* . 2>/dev/null || true
    rm -rf .git
    
    # Commit and push
    git add .
    git commit -m "ENVR Module Splitter - Complete implementation
    
    Mathematical theorem M = L ⊕ N implementation across 8 languages:
    - Python: Theorem verification
    - C++: High-performance
    - Java: Enterprise
    - Go: Concurrent
    - React/Next.js: Web visualization
    
    Deployed: $(date)
    System: $(hostname)
    "
    
    git push origin "$branch" --force
    
    echo "✅ Successfully pushed to $repo/$branch"
    
    # Cleanup
    cd ~/envr-module-splitter
    rm -rf "$TEMP_DIR"
}

# Push to each repository
for repo_entry in "${REPOS[@]}"; do
    repo="${repo_entry%:*}"
    branch="${repo_entry#*:}"
    
    # Check if repository exists
    if curl -s "https://api.github.com/repos/$repo" | grep -q "Not Found"; then
        echo "⚠️  Repository $repo does not exist. Skipping..."
        continue
    fi
    
    push_to_repo "$repo" "$branch"
done

echo -e "\n====================================================="
echo "✅ Push completed to all available repositories!"
echo "====================================================="
