#!/bin/bash
# Invite collaborators to repositories

echo "Inviting Collaborators to ENVR Repositories"
echo "==========================================="

# Collaborator list
COLLABORATORS=(
    "dt-uk/DENVR:muskan-dt"
    "shellworlds/AENVR:mike-aeq"
    "shellworlds/ZENVR:vipul-zius"
)

invite_collaborator() {
    local repo=$1
    local collaborator=$2
    
    echo "Inviting $collaborator to $repo..."
    
    # Using GitHub API to invite collaborator
    curl -X PUT \
      -H "Authorization: token $(cat ~/.github_token 2>/dev/null || echo '')" \
      -H "Accept: application/vnd.github.v3+json" \
      "https://api.github.com/repos/$repo/collaborators/$collaborator" \
      -d '{"permission":"push"}' && \
    echo "✅ Invitation sent to $collaborator for $repo" || \
    echo "⚠️  Failed to invite $collaborator (check permissions)"
}

# Invite each collaborator
for entry in "${COLLABORATORS[@]}"; do
    repo="${entry%:*}"
    collaborator="${entry#*:}"
    invite_collaborator "$repo" "$collaborator"
done

echo -e "\nCollaborator invitations completed!"
echo "Check GitHub for pending invitations."
