#!/bin/bash

# Deployment script for all client repositories
set -e

echo "ENVR Module Splitter Deployment Script"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to deploy to a repository
deploy_to_repo() {
    local repo_name=$1
    local branch_name=$2
    local repo_path="../envr-client-repos/${repo_name}"
    
    echo -e "\n${YELLOW}Deploying to ${repo_name} (branch: ${branch_name})...${NC}"
    
    if [ ! -d "$repo_path" ]; then
        echo -e "${RED}Repository not found: ${repo_path}${NC}"
        return 1
    fi
    
    # Copy all project files to repository
    echo "Copying files..."
    rsync -av --exclude='.git' --exclude='node_modules' --exclude='envr-client-repos' \
          ./ "$repo_path/" --delete
    
    # Navigate to repository
    cd "$repo_path"
    
    # Check if branch exists
    if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
        git checkout "$branch_name"
    else
        git checkout -b "$branch_name"
    fi
    
    # Add all files
    git add .
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        echo -e "${YELLOW}No changes to commit${NC}"
    else
        # Commit changes
        git commit -m "Deploy ENVR Module Splitter implementation
        
        Multi-language implementation of Module Splitting Theorem:
        - Python proof verification
        - C++ high-performance computation
        - Java enterprise implementation
        - Go concurrent verification
        - React/Next.js visualization
        - Build automation scripts
        
        System: $(hostname)
        Date: $(date)
        "
        
        # Push to remote
        echo "Pushing to remote repository..."
        if git push origin "$branch_name"; then
            echo -e "${GREEN}✓ Successfully deployed to ${repo_name}${NC}"
        else
            echo -e "${RED}✗ Failed to push to ${repo_name}${NC}"
            return 1
        fi
    fi
    
    # Return to project directory
    cd - > /dev/null
}

# List of repositories and branches (from config/branches.json)
REPOS=(
    "ZENVR:ZENVR41"
    "DENVR:DENVR41"
    "QENVR:QENVR41"
    "AENVR:AENVR41"
)

# Backup repositories
BACKUP_REPOS=(
    "shellworlds/ZENVR:ZENVR41"
    "shellworlds/DENVR:DENVR41"
    "shellworlds/QENVR:QENVR41"
    "shellworlds/AENVR:AENVR41"
    "shellworlds/ENVR:ENVR41"
)

echo -e "\n${GREEN}Deploying to Client Repositories${NC}"
echo "----------------------------------------"

for repo_entry in "${REPOS[@]}"; do
    repo="${repo_entry%%:*}"
    branch="${repo_entry##*:}"
    deploy_to_repo "$repo" "$branch"
done

echo -e "\n${GREEN}Deploying to Backup Repositories${NC}"
echo "-----------------------------------------"

for repo_entry in "${BACKUP_REPOS[@]}"; do
    repo="${repo_entry%%:*}"
    branch="${repo_entry##*:}"
    deploy_to_repo "$repo" "$branch"
done

echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}Deployment completed!${NC}"
echo -e "\nSummary of deployed repositories:"

cat > deployment_summary.md << 'SUMMARY'
# Deployment Summary

## Client Repositories
| Repository | Branch | Status |
|------------|--------|--------|
| ZENVR | ZENVR41 | ✓ Deployed |
| DENVR | DENVR41 | ✓ Deployed |
| QENVR | QENVR41 | ✓ Deployed |
| AENVR | AENVR41 | ✓ Deployed |

## Backup Repositories
| Repository | Branch | Status |
|------------|--------|--------|
| shellworlds/ZENVR | ZENVR41 | ✓ Deployed |
| shellworlds/DENVR | DENVR41 | ✓ Deployed |
| shellworlds/QENVR | QENVR41 | ✓ Deployed |
| shellworlds/AENVR | AENVR41 | ✓ Deployed |
| shellworlds/ENVR | ENVR41 | ✓ Deployed |

## Deployment Details
- Date: $(date)
- System: $(hostname)
- Total files: $(find . -type f -name "*.py" -o -name "*.cpp" -o -name "*.java" -o -name "*.go" -o -name "*.js" -o -name "*.jsx" -o -name "*.html" -o -name "*.css" -o -name "*.sh" -o -name "*.json" -o -name "*.md" | wc -l)
- Languages: Python, C++, Java, Go, JavaScript, React, Next.js, Shell

## Next Steps
1. Verify deployments on GitHub
2. Run tests on each implementation
3. Share with collaborators
SUMMARY

echo -e "\nDeployment summary saved to: deployment_summary.md"
echo -e "\n${YELLOW}Note:${NC} Check GitHub for proper branch creation and collaborator access."
