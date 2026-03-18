# What, why, how, when (team and implementation)

| Item | What | Why | How | When |
|------|------|-----|-----|------|
| System baseline | Capture OS, CPU, RAM, Git user | Avoid silent env drift | system_check.sh | Project kickoff |
| Toolchain | 16 tools per TOOLS_16.md | Reproducible builds | install_all_ubuntu.sh | Before first feature branch |
| Git identity | Author matches Vercel/org | Unblock CI deploy | git config per repo | Every client repo clone |
| Branch naming | ZENVR91, DENVR91, etc. | Traceability | push_client_branches.sh | Per deliverable |
| Handoff | POC_REPORT.md | Collaborator alignment | PR + branch URL | Milestone end |

Collaborators: muskan-dt (DENVR), mike-aeq (AENVR), vipul-zius (ZENVR), manav-2341 (BENVR).
