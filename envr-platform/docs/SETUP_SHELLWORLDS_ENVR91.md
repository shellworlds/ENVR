# ENVR91 on shellworlds/ENVR

Prefer the all-in-one script from ITMISAE repo root:

```bash
./envr-platform/scripts/setup_shellworlds_public_all.sh
```

That creates public repos if needed and pushes **main** plus **ENVR91** (and other REPO91 branches). Manual steps below if you only touch ENVR.

## One-time: clone and push ENVR91

Replace `PATH_TO_ITMISAE` with your local clone of BorelSigmaInc/ITMISAE.

```bash
export ITMISAE="$HOME/path/to/ITMISAE"
test -d "$ITMISAE/envr-platform" || { echo "Set ITMISAE to ITMISAE repo root"; exit 1; }

cd /tmp
rm -rf shellworlds-ENVR-setup
git clone git@github.com:shellworlds/ENVR.git shellworlds-ENVR-setup
cd shellworlds-ENVR-setup

git fetch origin
git checkout main 2>/dev/null || git checkout master 2>/dev/null || true
git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true

git checkout -B ENVR91
rm -rf envr-platform
cp -a "$ITMISAE/envr-platform" .
git add envr-platform
git status
git commit -m "feat(envr): ENVR platform toolkit branch ENVR91" || echo "nothing to commit"
git push -u origin ENVR91
```

Then open: https://github.com/shellworlds/ENVR/tree/ENVR91

## If clone fails

- Repo missing: create **shellworlds/ENVR** on GitHub (empty repo), then run again.
- Permission denied: add SSH key to GitHub account **shellworlds**; test `ssh -T git@github.com`.
- Repo is organization-owned: ensure **shellworlds** has write access.

## If push rejects author

Match Vercel/org policy if this repo triggers deploys:

```bash
git config user.name "shellworlds"
git config user.email "rr@q-bit.space"
```

Then amend and push:

```bash
git commit --amend --reset-author --no-edit
git push -u origin ENVR91 --force-with-lease
```
