# Five processes for client problem statements

## P1 Baseline audit

Run `step-01/system_check.sh` and archive output. Establishes OS, CPU, RAM, disk, Git identity before any deploy.

## P2 Toolchain alignment

Run `scripts/install_all_ubuntu.sh` then `scripts/verify_toolchain.sh`. Ensures build and runtime parity across dev laptops.

## P3 Git identity and branch policy

Per organization, set `git config user.name` and `user.email` to addresses recognized by Vercel/GitHub orgs. Create feature branches named per client convention (e.g. ZENVR91).

## P4 CI and deploy gate

Push only after author/committer matches team policy. Optional: GitHub Actions or Vercel project settings to enforce allowed committers.

## P5 Documentation and handoff

Update POC_REPORT.md and WHAT_WHY_HOW_WHEN.md after each milestone. Collaborators (muskan-dt, mike-aeq, vipul-zius, manav-2341) receive branch URLs and role notes via client repos.
