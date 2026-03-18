#!/usr/bin/env bash
# Push envr-platform to github.com/shellworlds/ENVR branch ENVR91 only.
# Usage: ITMISAE=/path/to/ITMISAE ./push_shellworlds_ENVR91.sh

set -euo pipefail
ITMISAE="${ITMISAE:-$(cd "$(dirname "$0")/../../.." && pwd)}"
SRC="$ITMISAE/envr-platform"
test -d "$SRC" || { echo "Missing $SRC — set ITMISAE to ITMISAE repo root"; exit 1; }

WORKDIR="${TMPDIR:-/tmp}/shellworlds-ENVR-$$"
git clone git@github.com:shellworlds/ENVR.git "$WORKDIR"
cd "$WORKDIR"
git fetch origin
git checkout main 2>/dev/null || git checkout master 2>/dev/null || true
git pull 2>/dev/null || true
git checkout -B ENVR91
rm -rf envr-platform
cp -a "$SRC" ./envr-platform
git add envr-platform
git commit -m "feat(envr): ENVR platform ENVR91" || true
git push -u origin ENVR91
echo "Done: https://github.com/shellworlds/ENVR/tree/ENVR91"
