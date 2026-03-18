# Notify collaborators (email and GitHub)

You must send email from your own mailbox and complete GitHub steps in the browser or with `gh`. This file supplies text and procedures only.

## Accounts and emails (from your list)

| GitHub-style handle | Email | Suggested repo focus |
|---------------------|-------|----------------------|
| muskan-dt | muskan.s@data-t.space | DENVR line, dt-uk context |
| mike-aeq | mike.s@a-eq.com | AENVR, shellworlds/AENVR |
| vipul-zius | vipul.j@zi-us.com | ZENVR, shellworlds/ZENVR |
| manav-2341 | manav2341 | crm@borelsigma.in, BENVR |

Public toolkit base: **https://github.com/shellworlds/ENVR** (branch ENVR91). Mirrors: ZENVR, DENVR, QENVR, AENVR, BENVR under **github.com/shellworlds**.

---

## A. Email (copy subject and body; send from your email client)

### To muskan.s@data-t.space

Subject: ENVR public toolkit on GitHub shellworlds — collaboration / fork

Body:

```
We published the ENVR environment and deployment toolkit as public repositories under github.com/shellworlds (ENVR, DENVR, and related mirrors). Please review https://github.com/shellworlds/ENVR/tree/ENVR91 and fork or collaborate as agreed for the DENVR line. Reply if you need repository access or a different branch layout.

Regards
```

### To mike.s@a-eq.com

Subject: ENVR public repos — AENVR / shellworlds collaboration

Body:

```
The ENVR toolkit is available on public GitHub under shellworlds (see https://github.com/shellworlds/AENVR/tree/AENVR91 and the aggregate https://github.com/shellworlds/ENVR). Please fork or accept a GitHub collaborator invite on the repos you need. Contact us for access or integration questions.

Regards
```

### To vipul.j@zi-us.com

Subject: ENVR public toolkit — ZENVR mirror on shellworlds

Body:

```
Public ENVR documentation and scripts are on https://github.com/shellworlds/ZENVR/tree/ZENVR91 (and shellworlds/ENVR). You are welcome to fork or collaborate via GitHub. We can add you as a collaborator on specific repositories on request.

Regards
```

### To crm@borelsigma.in (manav-2341 / BENVR)

Subject: ENVR BENVR public mirror — fork and collaboration

Body:

```
ENVR public artifacts are published under https://github.com/shellworlds/BENVR/tree/BENVR91 and the canonical https://github.com/shellworlds/ENVR. Please fork or request collaborator access for the BENVR track. POC and process docs live under envr-platform/ in each repo.

Regards
```

---

## B. GitHub notifications (no bulk email from GitHub to arbitrary addresses)

GitHub notifies users when:

1. **Collaborator invite:** Settings → Collaborators → add their **GitHub username** (not email). They get an email from GitHub if notifications are on.
2. **@mention:** Open an **Issue** on e.g. shellworlds/ENVR and comment `@muskan-dt @mike-aeq @vipul-zius @manav2341` (use exact usernames). Each mentioned user gets a GitHub notification if they use that account.
3. **Team / org:** If they are in your GitHub org, add them to a team with repo access.

### Suggested issue (create once per repo or only on ENVR)

Title: Collaboration and forks — ENVR public toolkit

Body:

```
Public ENVR toolkit is on main and ENVR91 (or matching REPO91 branch).

@muskan-dt @mike-aeq @vipul-zius @manav2341

Please fork this repository or reply here if you need collaborator access. Email outreach was sent separately.

Links:
- https://github.com/shellworlds/ENVR/tree/ENVR91
- PUBLIC_SHELLWORLDS_URLS.md in repo for all shellworlds URLs
```

Create the issue after `setup_shellworlds_public_all.sh` has run so the repo exists.

### gh CLI (optional, run locally after auth)

```bash
gh issue create --repo shellworlds/ENVR \
  --title "Collaboration: fork or request access" \
  --body "See NOTIFY_COLLABORATORS.md in envr-platform/docs. @muskan-dt @mike-aeq @vipul-zius @manav2341"
```

Replace @handles with real GitHub usernames if different.

---

## C. Limitations

- This project cannot send SMTP email or impersonate your domain.
- GitHub does not send platform notifications to email addresses that are not linked to a GitHub account for @mentions; collaborator invites require the invitee’s GitHub username.
