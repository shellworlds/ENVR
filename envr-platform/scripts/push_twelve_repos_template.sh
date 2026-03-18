#!/usr/bin/env bash
# Template: push envr-platform to 6 client orgs + 6 shellworlds mirrors.
# Run on ThinkPad with SSH write to EVERY remote. One repo at a time recommended.
# GIT_AUTHOR_NAME=shellworlds GIT_AUTHOR_EMAIL=rr@q-bit.space

set -euo pipefail
ENVR_SRC="${ENVR_SRC:-$(cd "$(dirname "$0")/.." && pwd)}"
NAME="${GIT_AUTHOR_NAME:-shellworlds}"
EMAIL="${GIT_AUTHOR_EMAIL:-rr@q-bit.space}"
WORKDIR="${WORKDIR:-$HOME/envr-twelve-$$}"
mkdir -p "$WORKDIR"

declare -a PAIRS=(
  "Zius-Global/ZENVR:ZENVR91"
  "dt-uk/DENVR:DENVR91"
  "qb-eu/QENVR:QENVR91"
  "vipul-zius/ZENVR:ZENVR91"
  "mike-aeq/AENVR:AENVR91"
  "manav2341/BENVR:BENVR91"
  "shellworlds/ZENVR:ZENVR91"
  "shellworlds/DENVR:DENVR91"
  "shellworlds/QENVR:QENVR91"
  "shellworlds/AENVR:AENVR91"
  "shellworlds/ENVR:ENVR91"
  "shellworlds/BENVR:BENVR91"
)

for pair in "${PAIRS[@]}"; do
  repo="${pair%%:*}"
  br="${pair##*:}"
  safe="${repo//\//_}"
  echo "=== $repo -> $br ==="
  T="$WORKDIR/$safe"
  rm -rf "$T"
  git clone "git@github.com:${repo}.git" "$T" || { echo "SKIP $repo"; continue; }
  cd "$T"
  git fetch origin
  git checkout -B "$br" 2>/dev/null || git checkout -B "$br" origin/main 2>/dev/null || git checkout -B "$br" origin/master 2>/dev/null || git checkout -B "$br"
  rm -rf envr-platform
  cp -a "$ENVR_SRC" ./envr-platform
  git add envr-platform
  GIT_AUTHOR_NAME="$NAME" GIT_AUTHOR_EMAIL="$EMAIL" \
  GIT_COMMITTER_NAME="$NAME" GIT_COMMITTER_EMAIL="$EMAIL" \
  git commit -m "feat(envr): toolkit branch ${br}" || true
  git push -u origin "$br" || echo "PUSH FAILED $repo"
done
rm -rf "$WORKDIR"
echo "Done."
