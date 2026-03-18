# Why you see 404

## URL you type (never works on GitHub)

```
https://github.com/shellworlds/ZENVR/ZENVR91
```

There is no page at `owner/repo/BRANCHNAME` as three path segments. This is not fixable by making the repo public. It is the wrong address.

## URL that works after the branch exists

```
https://github.com/shellworlds/ZENVR/tree/ZENVR91
```

Note the word **tree** between the repo name and the branch.

## Current state (verified via GitHub API)

Repos **shellworlds/ENVR, ZENVR, DENVR, QENVR, AENVR, BENVR** are public, but branches **ENVR91, ZENVR91, DENVR91, QENVR91, AENVR91, BENVR91 do not exist yet.** Until you push them, even the correct `/tree/ZENVR91` link returns 404.

## Finish in one run (ThinkPad, Ubuntu)

You need **push access** to **shellworlds** on GitHub.

### Option A: SSH (if `git@github.com` works as shellworlds)

```bash
export ITMISAE=/path/to/your/clone/ITMISAE
chmod +x "$ITMISAE/envr-platform/scripts/push_six_branches_ssh.sh"
"$ITMISAE/envr-platform/scripts/push_six_branches_ssh.sh"
```

### Option B: HTTPS with personal access token

Create a classic PAT for account **shellworlds** with **repo** scope. Then:

```bash
export ITMISAE=/path/to/your/clone/ITMISAE
export GITHUB_TOKEN=ghp_your_token_here
chmod +x "$ITMISAE/envr-platform/scripts/push_six_branches_https.sh"
"$ITMISAE/envr-platform/scripts/push_six_branches_https.sh"
```

Unset the token after: `unset GITHUB_TOKEN`

### After success, open

- https://github.com/shellworlds/ZENVR/tree/ZENVR91
- https://github.com/shellworlds/ENVR/tree/ENVR91
- Same pattern for DENVR, QENVR, AENVR, BENVR.

Still do not use `github.com/shellworlds/ZENVR/ZENVR91`.
