# Review: original prompt vs current delivery

Reference: your specification (Lenovo ThinkPad, AMD Gen5, Ubuntu, 32 GB RAM, 1 TB SSD; ENVR program; client and shellworlds repos; one step at a time).

## One step at a time (your rule)

You required **only one step per cycle, next step after your feedback**. Bulk pushes to twelve remotes and multi-step automation conflict with that rule. Agreed mode going forward:

| Mode | Action |
|------|--------|
| Strict | Reply with which single step to run next (e.g. "Step: push shellworlds/ENVR only"). |
| Waived | You explicitly say "run all pushes" then execute full `setup_shellworlds_public_all.sh` and separate client-remote script on your machine. |

## Requirement checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| Problem in INDEX | Done | INDEX.md (Vercel commit-author case + ENVR scope). |
| Min 8 files, languages: py, shell, react, node, next, vite, java, html, c++, go | Done | Under `src/` and `step-01/`; Next as `next-page-stub.tsx`. |
| 16 tools | Done | docs/TOOLS_16.md |
| 5 processes | Done | docs/PROCESSES_5.md |
| Generic, start with system check + OS | Done | step-01/system_check.sh |
| Lenovo / Mac / Windows install text | Done | docs/INSTALL_LENOVO_UBUNTU.md, INSTALL_MAC.md, INSTALL_WINDOWS.md |
| One-shot Ubuntu install | Done | scripts/install_all_ubuntu.sh |
| POC report, skills, packages, client next step | Done | POC_REPORT.md |
| What / why / how / when table | Done | docs/WHAT_WHY_HOW_WHEN.md |
| No emoticons / fancy icons | Done | Plain text in toolkit files. |
| Git identity shellworlds for client-facing work | Partial | Commits on **BorelSigmaInc/ITMISAE** use corporate author for deploy policy; on **shellworlds** remotes use `GIT_AUTHOR_NAME=shellworlds` when you push from ThinkPad. |
| New branches ZENVR91, DENVR91, etc. | Partial | Branch names defined; **pushes to GitHub must run on your machine** with SSH. |
| Push to Zius-Global/ZENVR, dt-uk/DENVR, qb-eu/QENVR, vipul-zius/ZENVR, mike-aeq/AENVR, manav2341/BENVR | **Not done from Cursor** | No credentials to those orgs in this environment. Script template: restore `push_client_branches.sh` multi-remote map or run per-repo `git push` from your laptop. |
| Push to shellworlds/ZENVR, DENVR, QENVR, AENVR, ENVR, BENVR | **Not done from Cursor** | Requires **shellworlds** `gh` + SSH. Command: `./envr-platform/scripts/setup_shellworlds_public_all.sh`. |
| Table: URLs + max 25 words per repo | Done | REPO_MATRIX.md (shellworlds-only in current matrix); extend table when client URLs are live. |
| Collaborator emails (muskan-dt, mike-aeq, vipul-zius, manav-2341) | Documented | docs/NOTIFY_COLLABORATORS.md; you send email and GitHub invites. |

## GitHub URL you tried

`https://github.com/shellworlds/ZENVR/ZENVR91` is **not a valid GitHub URL**. Use:

- `https://github.com/shellworlds/ZENVR/tree/ZENVR91` or
- `https://github.com/shellworlds/ZENVR` after default branch is set to ZENVR91 by setup script.

See ACCESS_GITHUB.md.

## Suggested next single step (after your reply)

Reply with **one** of:

1. **Step A:** Push only **shellworlds/ENVR** branch ENVR91 (you run commands from NOTIFY or setup script scoped to one repo).
2. **Step B:** Restore and document **one** client remote push (e.g. dt-uk/DENVR) with exact copy-paste block.
3. **Step C:** Adjust REPO_MATRIX to list **both** client org URLs and shellworlds URLs in one table (no push).

No further multi-repo execution until you name the step.
