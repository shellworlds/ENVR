#!/bin/bash
# File: push_to_repos.sh
# Purpose: Push project files to all client repositories

set -e

PROJECT_ROOT="$HOME/ENVR_Project"
cd "$PROJECT_ROOT"

echo "=============================================="
echo "Pushing Files to Client Repositories"
echo "=============================================="

# Define branch names for each repo
declare -A branch_names=(
    ["Zius-Global_ZENVR"]="ZENVR43"
    ["dt-uk_DENVR"]="DENVR43"
    ["qb-eu_QENVR"]="QENVR43"
    ["vipul-zius_ZENVR"]="ZENVR43"
    ["mike-aeq_AENVR"]="AENVR43"
    ["manav2341_BENVR"]="BENVR43"
    ["muskan-dt_DENVR"]="DENVR43"
    ["shellworlds_ENVR"]="ENVR43"
)

# Backup repositories use same branch names
declare -A backup_branch_names=(
    ["shellworlds_ZENVR"]="ZENVR43"
    ["shellworlds_DENVR"]="DENVR43"
    ["shellworlds_QENVR"]="QENVR43"
    ["shellworlds_AENVR"]="AENVR43"
    ["shellworlds_ENVR"]="ENVR43"
    ["shellworlds_BENVR"]="BENVR43"
)

# Function to push to a repository
push_to_repo() {
    local repo_dir=$1
    local branch_name=$2
    local repo_display_name=$3
    
    echo ""
    echo "Processing: $repo_display_name"
    echo "Directory: $repo_dir"
    echo "Branch: $branch_name"
    
    if [ ! -d "$repo_dir" ]; then
        echo "Repository directory not found: $repo_dir"
        return 1
    fi
    
    cd "$repo_dir"
    
    # Check if we're in a git repository
    if [ ! -d ".git" ]; then
        echo "Not a git repository: $repo_dir"
        cd "$PROJECT_ROOT"
        return 1
    fi
    
    # Create or switch to branch
    git checkout -b "$branch_name" 2>/dev/null || git checkout "$branch_name" 2>/dev/null
    
    # Remove existing files (except .git)
    echo "Cleaning repository..."
    find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} + 2>/dev/null || true
    
    # Copy all project files
    echo "Copying project files..."
    cp -r "$PROJECT_ROOT"/src . 2>/dev/null || true
    cp -r "$PROJECT_ROOT"/api . 2>/dev/null || true
    cp -r "$PROJECT_ROOT"/scripts . 2>/dev/null || true
    cp -r "$PROJECT_ROOT"/docs . 2>/dev/null || true
    cp -r "$PROJECT_ROOT"/config . 2>/dev/null || true
    cp -r "$PROJECT_ROOT"/docker . 2>/dev/null || true
    cp -r "$PROJECT_ROOT"/tests . 2>/dev/null || true
    cp "$PROJECT_ROOT"/Makefile . 2>/dev/null || true
    cp "$PROJECT_ROOT"/README.md . 2>/dev/null || true
    cp "$PROJECT_ROOT"/requirements.txt . 2>/dev/null || true
    cp "$PROJECT_ROOT"/branch_mapping.txt . 2>/dev/null || true
    
    # Remove the repositories directory if it was copied
    rm -rf repositories 2>/dev/null || true
    
    # Add all files
    git add .
    
    # Check if there are changes
    if git status --porcelain | grep -q .; then
        echo "Committing changes..."
        git commit -m "Add projective module theorem implementation
        
        Implementations in multiple languages:
        - Python: Complete theorem proofs
        - C++: High-performance computation
        - Java: Object-oriented design
        - Go: Concurrent verification
        - JavaScript/Node.js: Web API
        - Shell: Automation scripts
        - HTML/CSS: Web interface
        - Make: Build automation
        
        Includes:
        - All 4 projective module theorems
        - Test suites
        - Documentation
        - Deployment scripts
        - Docker configuration
        - API server
        
        Created by: shellworlds
        System: Lenovo ThinkPad P14s Gen5 AMD, Ubuntu 24.04
        Date: $(date +%Y-%m-%d)"
        
        # Push to remote
        echo "Pushing to remote repository..."
        if git push origin "$branch_name"; then
            echo "✓ Successfully pushed to $repo_display_name"
        else
            echo "⚠ Push failed for $repo_display_name"
        fi
    else
        echo "No changes to commit for $repo_display_name"
    fi
    
    cd "$PROJECT_ROOT"
}

# Push to client repositories
echo ""
echo "Pushing to CLIENT repositories..."
for repo_dir in repositories/clients/*; do
    if [ -d "$repo_dir" ]; then
        repo_key=$(basename "$repo_dir")
        branch_name="${branch_names[$repo_key]}"
        
        if [ ! -z "$branch_name" ]; then
            push_to_repo "$repo_dir" "$branch_name" "$repo_key"
        else
            echo "No branch mapping for: $repo_key"
        fi
    fi
done

# Push to backup repositories
echo ""
echo "Pushing to BACKUP repositories..."
for repo_dir in repositories/backups/*; do
    if [ -d "$repo_dir" ]; then
        repo_key=$(basename "$repo_dir")
        # Use same branch names for backups
        branch_name="${branch_names[${repo_key#shellworlds_}]}"
        
        if [ ! -z "$branch_name" ]; then
            push_to_repo "$repo_dir" "$branch_name" "$repo_key"
        else
            echo "No branch mapping for: $repo_key"
        fi
    fi
done

echo ""
echo "=============================================="
echo "Push Operation Complete"
echo "=============================================="
echo "Summary of repositories pushed:"
echo ""
echo "Client Repositories:"
for repo_key in "${!branch_names[@]}"; do
    echo "  - $repo_key : ${branch_names[$repo_key]}"
done
echo ""
echo "Next: Check GitHub for pull requests and verify pushes"
echo "=============================================="
