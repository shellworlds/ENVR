# ENVR Platform Index

**404 on links:** Read **START_HERE.md**. Wrong URL pattern plus missing **ZENVR91** (and other *91) branches. Run **scripts/push_six_branches_ssh.sh** or **push_six_branches_https.sh** on your ThinkPad as **shellworlds**.

## Problem reference

Vercel (and similar) may block deployments when **Git author/committer** email is not recognized on the hosting team. Fix: align Git identity with org-approved emails or adjust platform access rules.

## Deliverable layout

| Path | Purpose |
|------|---------|
| step-01/system_check.sh | OS and hardware baseline |
| scripts/install_all_ubuntu.sh | One-shot Ubuntu package install |
| scripts/verify_toolchain.sh | Post-install verification |
| docs/TOOLS_16.md | Sixteen toolchain items |
| docs/PROCESSES_5.md | Five client-facing processes |
| docs/INSTALL_*.md | Lenovo Ubuntu, Mac, Windows WSL |
| src/* | Python, Node, Go, C++, Java, HTML, React TSX, Vite stub |
| POC_REPORT.md | Skills, tools, next steps |
| docs/WHAT_WHY_HOW_WHEN.md | Team and implementation table |
| scripts/push_client_branches.sh | Template for multi-repo branch push |

## Maintainer

Primary Git identity for client branches: **shellworlds** (set per-repo `user.email` per client policy).

## Prompt compliance review

**docs/PROMPT_COMPLIANCE_REVIEW.md** maps your original specification to delivered files, gaps, and the one-step-at-a-time rule.

## Collaborator outreach

Email templates and GitHub issue / invite steps: **docs/NOTIFY_COLLABORATORS.md** (you send mail and create issues; automation cannot email third parties from here).

## Public hosting (shellworlds only)

Canonical public URLs: **PUBLIC_SHELLWORLDS_URLS.md**. Create and update all six public repos:

`./scripts/setup_shellworlds_public_all.sh` (after `gh auth login` and SSH as shellworlds).
