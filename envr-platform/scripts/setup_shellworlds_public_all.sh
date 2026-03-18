#!/usr/bin/env bash
# Public github.com/shellworlds repos: create if missing, push toolkit to main + REPO91.
# gh auth login && SSH shellworlds required.

set -euo pipefail
OWNER="shellworlds"
ENVR_SRC="$(cd "$(dirname "$0")/.." && pwd)"
WORKDIR="${TMPDIR:-/tmp}/sw-public-$$"
NAME="${GIT_AUTHOR_NAME:-shellworlds}"
EMAIL="${GIT_AUTHOR_EMAIL:-rr@q-bit.space}"

command -v gh >/dev/null 2>&1 || { echo "Install GitHub CLI: https://cli.github.com"; exit 1; }

mkdir -p "${WORKDIR}"
trap 'rm -rf "${WORKDIR}"' EXIT

for REPO in ENVR ZENVR DENVR QENVR AENVR BENVR; do
  BRANCH="${REPO}91"
  FULL="${OWNER}/${REPO}"
  echo "=== ${FULL} public -> main + ${BRANCH} ==="

  if ! gh repo view "${FULL}" &>/dev/null; then
    gh repo create "${FULL}" --public --description "ENVR public toolkit ${REPO}"
    sleep 2
  fi
  gh repo edit "${FULL}" --visibility public 2>/dev/null || true

  D="${WORKDIR}/${REPO}"
  rm -rf "${D}"
  mkdir -p "${D}"
  cd "${D}"

  if ! git clone "git@github.com:${FULL}.git" . 2>/dev/null; then
    git init
    git remote add origin "git@github.com:${FULL}.git"
  fi

  rm -rf envr-platform
  cp -a "${ENVR_SRC}" ./envr-platform
  cp -f "${ENVR_SRC}/LICENSE" ./LICENSE 2>/dev/null || true
  {
    echo "# ${REPO}"
    echo "Public ENVR toolkit. See [ACCESS_GITHUB.md](envr-platform/ACCESS_GITHUB.md) if a link failed."
    echo "Default branch after setup: **${BRANCH}**. Main and ${BRANCH} point to same commit."
  } > README.md

  git add -A
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    if git diff --staged --quiet; then
      echo "No file changes."
    else
      GIT_AUTHOR_NAME="${NAME}" GIT_AUTHOR_EMAIL="${EMAIL}" \
      GIT_COMMITTER_NAME="${NAME}" GIT_COMMITTER_EMAIL="${EMAIL}" \
      git commit -m "feat(envr): update public toolkit ${REPO}"
    fi
  else
    GIT_AUTHOR_NAME="${NAME}" GIT_AUTHOR_EMAIL="${EMAIL}" \
    GIT_COMMITTER_NAME="${NAME}" GIT_COMMITTER_EMAIL="${EMAIL}" \
    git commit -m "feat(envr): initial public toolkit ${REPO}"
  fi

  git branch -M main 2>/dev/null || true
  git push -u origin main

  git branch -f "${BRANCH}" HEAD
  git push -u origin "${BRANCH}" --force

  echo "Set repo public + default branch to ${BRANCH} (so github.com/${FULL} opens this branch)"
  gh repo edit "${FULL}" --visibility public 2>/dev/null || true
  gh api "repos/${FULL}" -X PATCH -f "default_branch=${BRANCH}" 2>/dev/null || \
    echo "WARN: set default branch to ${BRANCH} manually in GitHub Settings if API failed"

  echo "OPEN: https://github.com/${FULL}"
  echo "TREE: https://github.com/${FULL}/tree/${BRANCH}"
done

echo "Finished. Wrong URL github.com/shellworlds/ZENVR/ZENVR91 is invalid; use links above."
