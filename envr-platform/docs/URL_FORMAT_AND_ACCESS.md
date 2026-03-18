# Why a link fails and the correct URL shape

## Wrong (404 on GitHub)

```
https://github.com/shellworlds/ZENVR/ZENVR91
```

GitHub does not use `owner/repo/branch` in that form. That path is invalid.

## Correct (branch view)

```
https://github.com/shellworlds/ZENVR/tree/ZENVR91
```

You must include **`/tree/`** before the branch name: `.../REPO/tree/BRANCH`.

## Correct (repo home, default branch)

```
https://github.com/shellworlds/ZENVR
```

If the repo exists and is public, this works even when you have not created `ZENVR91` yet.

## If the correct URL still returns 404

| Symptom | Cause | Fix |
|---------|--------|-----|
| 404 on `.../shellworlds/ZENVR` | Repo never created or wrong owner name | Create public repo **ZENVR** under user **shellworlds**, or run `setup_shellworlds_public_all.sh` |
| Repo loads but **ZENVR91** missing | Branch never pushed | Run `./envr-platform/scripts/setup_shellworlds_public_all.sh` from your machine with `gh auth login` and SSH |
| 404 or private | Repo private | Settings → General → Change visibility → Public |

## Copy-paste list (valid URLs)

- https://github.com/shellworlds/ENVR/tree/ENVR91
- https://github.com/shellworlds/ZENVR/tree/ZENVR91
- https://github.com/shellworlds/DENVR/tree/DENVR91
- https://github.com/shellworlds/QENVR/tree/QENVR91
- https://github.com/shellworlds/AENVR/tree/AENVR91
- https://github.com/shellworlds/BENVR/tree/BENVR91
