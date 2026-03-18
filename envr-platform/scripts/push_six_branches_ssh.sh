#!/usr/bin/env bash
# Creates and pushes ENVR91, ZENVR91, ... on shellworlds/* using SSH.
# Requires: git@github.com:shellworlds/*.git push access
set -euo pipefail
ENVR_SRC="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${GIT_AUTHOR_NAME:-shellworlds}"
EMAIL="${GIT_AUTHOR_EMAIL:-rr@q-bit.space}"
TMP="${TMPDIR:-/tmp}/sw91-ssh-$$"
mkdir -p "$TMP"
trap 'rm -rf "$TMP"' EXIT

for REPO in ENVR ZENVR DENVR QENVR AENVR BENVR; do
  BR="${REPO}91"
  FULL="shellworlds/${REPO}"
  D="$TMP/$REPO"
  rm -rf "$D"
  git clone "git@github.com:${FULL}.git" "$D"
  cd "$D"
  git fetch origin
  git checkout main 2>/dev/null || git checkout master 2>/dev/null || true
  git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
  git checkout -B "$BR"
  rm -rf envr-platform
  cp -a "$ENVR_SRC" ./envr-platform
  cp -f "$ENVR_SRC/LICENSE" ./LICENSE 2>/dev/null || true
  echo "# ${REPO} branch ${BR}" > README.md
  echo "Toolkit: [envr-platform/README.md](envr-platform/README.md)" >> README.md
  echo "Correct URL: https://github.com/${FULL}/tree/${BR}" >> README.md
  git add -A
  GIT_AUTHOR_NAME="$NAME" GIT_AUTHOR_EMAIL="$EMAIL" \
  GIT_COMMITTER_NAME="$NAME" GIT_COMMITTER_EMAIL="$EMAIL" \
  git commit -m "feat(envr): toolkit ${BR}" || true
  git push -u "git@github.com:${FULL}.git" "$BR" --force
  echo "OK https://github.com/${FULL}/tree/${BR}"
done
echo "Done. Do not use .../ZENVR/ZENVR91 (invalid). Use .../ZENVR/tree/ZENVR91"
