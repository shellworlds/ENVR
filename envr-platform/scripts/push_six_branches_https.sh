#!/usr/bin/env bash
# Same as push_six_branches_ssh.sh but HTTPS with GITHUB_TOKEN (shellworlds PAT, repo scope).
set -euo pipefail
test -n "${GITHUB_TOKEN:-}" || { echo "Set GITHUB_TOKEN (shellworlds classic PAT with repo scope)"; exit 1; }
ENVR_SRC="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${GIT_AUTHOR_NAME:-shellworlds}"
EMAIL="${GIT_AUTHOR_EMAIL:-rr@q-bit.space}"
TMP="${TMPDIR:-/tmp}/sw91-https-$$"
mkdir -p "$TMP"
trap 'rm -rf "$TMP"' EXIT

for REPO in ENVR ZENVR DENVR QENVR AENVR BENVR; do
  BR="${REPO}91"
  FULL="shellworlds/${REPO}"
  D="$TMP/$REPO"
  rm -rf "$D"
  git clone "https://github.com/${FULL}.git" "$D"
  cd "$D"
  git fetch origin
  git checkout main 2>/dev/null || git checkout master 2>/dev/null || true
  git pull 2>/dev/null || true
  git checkout -B "$BR"
  rm -rf envr-platform
  cp -a "$ENVR_SRC" ./envr-platform
  cp -f "$ENVR_SRC/LICENSE" ./LICENSE 2>/dev/null || true
  echo "# ${REPO} branch ${BR}" > README.md
  echo "https://github.com/${FULL}/tree/${BR}" >> README.md
  git add -A
  GIT_AUTHOR_NAME="$NAME" GIT_AUTHOR_EMAIL="$EMAIL" \
  GIT_COMMITTER_NAME="$NAME" GIT_COMMITTER_EMAIL="$EMAIL" \
  git commit -m "feat(envr): toolkit ${BR}" || true
  git remote set-url origin "https://shellworlds:${GITHUB_TOKEN}@github.com/${FULL}.git"
  git push -u origin "$BR" --force
  git remote set-url origin "https://github.com/${FULL}.git"
  echo "OK https://github.com/${FULL}/tree/${BR}"
done
echo "Done. Run: unset GITHUB_TOKEN when finished."
