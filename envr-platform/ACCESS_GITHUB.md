# GitHub access: read this first

## This URL never works on GitHub (404 forever)

```
https://github.com/shellworlds/ZENVR/ZENVR91
```

GitHub has no route `github.com/USER/REPO/BRANCH`. The third segment is not a branch name. Making the repo public does not change that.

## URLs that work

After the repository exists and is **public**, use:

1. **Repo home (default branch is set to ZENVR91 after setup script):**  
   https://github.com/shellworlds/ZENVR

2. **Explicit branch:**  
   https://github.com/shellworlds/ZENVR/tree/ZENVR91

## If you still see nothing

The repository may not exist yet. On your computer, as user **shellworlds**:

```bash
gh auth login
cd /path/to/ITMISAE
./envr-platform/scripts/setup_shellworlds_public_all.sh
```

That creates **public** repos, pushes code, and sets **default branch** to ZENVR91 (and ENVR91, DENVR91, etc.) so the short link **github.com/shellworlds/ZENVR** opens the right branch.
