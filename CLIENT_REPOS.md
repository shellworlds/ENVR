# SN-112BA Client Repositories and Push Commands

Main developer: shellworlds. Push to each repo on the branch listed. Run from project root after: git add -A && git commit -m "SN-112BA POC full"

## Table: URLs, branch, and skill post (max 25 words)

| Repo | URL | Branch | Skill post (max 25 words) |
|------|-----|--------|---------------------------|
| Zius-Global/ZENVR | https://github.com/Zius-Global/ZENVR | ZENVR72 | Quantum QFT, FedStress, PSO, Kyber, full-stack Python Node React Java C++ Go, 10 graphs, Watson stub, edge. |
| dt-uk/DENVR | https://github.com/dt-uk/DENVR | DENVR72 | SN-112BA federated stress, biometric, swarm PSO, API and dashboard, 20q QFT sim, post-quantum handshake. |
| qb-eu/QENVR | https://github.com/qb-eu/QENVR | QENVR72 | 20-qubit QFT, quantum-phase and stress maps, PSO swarm, Kyber sim, React Node Python Java C++ Go. |
| vipul-zius/ZENVR | https://github.com/vipul-zius/ZENVR | ZENVR72 | Quantum-cognitive stack: Qiskit QFT, FedStress, PSO, Kyber, biometric, Watson, 2D/3D graphs, 4s GIF. |
| mike-aeq/AENVR | https://github.com/mike-aeq/AENVR | AENVR72 | Edge POC: QFT, FedStress, PSO, Kyber, Node API, React/Vite/Next, Java C++ Go, 10 graphs, install script. |
| muskan-dt/DENVR | https://github.com/muskan-dt/DENVR | DENVR72 | Federated stress detection, biometric signals, swarm coordination, quantum sim, full API and dashboards. |
| shellworlds/ZENVR | https://github.com/shellworlds/ZENVR | ZENVR72 | Backup/collab: same as Zius-Global delivery branch. |
| shellworlds/DENVR | https://github.com/shellworlds/DENVR | DENVR72 | Backup/collab: same as dt-uk delivery branch. |
| shellworlds/QENVR | https://github.com/shellworlds/QENVR | QENVR72 | Backup/collab: same as qb-eu delivery branch. |
| shellworlds/AENVR | https://github.com/shellworlds/AENVR | AENVR72 | Backup/collab: same as mike-aeq delivery branch. |
| shellworlds/ENVR | https://github.com/shellworlds/ENVR | main or sn112ba | Primary; SN-112BA full POC. |

## Copy-paste: add remotes and push (Ubuntu/Lenovo)

Ensure SSH is set and you have write access. Replace ORIGIN with your main remote if needed.

```bash
cd /home/rrmr/Desktop/RRMR/BProjects/BorelSIgmaInc/SN112BA

# Create branches if not already
git branch ZENVR72 2>/dev/null || true
git branch DENVR72 2>/dev/null || true
git branch QENVR72 2>/dev/null || true
git branch AENVR72 2>/dev/null || true

# Client remotes (add once)
git remote add zius-global git@github.com:Zius-Global/ZENVR.git 2>/dev/null || true
git remote add dt-uk git@github.com:dt-uk/DENVR.git 2>/dev/null || true
git remote add qb-eu git@github.com:qb-eu/QENVR.git 2>/dev/null || true
git remote add vipul-zius git@github.com:vipul-zius/ZENVR.git 2>/dev/null || true
git remote add mike-aeq git@github.com:mike-aeq/AENVR.git 2>/dev/null || true
git remote add muskan-dt git@github.com:muskan-dt/DENVR.git 2>/dev/null || true
git remote add sw-z git@github.com:shellworlds/ZENVR.git 2>/dev/null || true
git remote add sw-d git@github.com:shellworlds/DENVR.git 2>/dev/null || true
git remote add sw-q git@github.com:shellworlds/QENVR.git 2>/dev/null || true
git remote add sw-a git@github.com:shellworlds/AENVR.git 2>/dev/null || true
git remote add sw-envr git@github.com:shellworlds/ENVR.git 2>/dev/null || true

# Push ZENVR72 to Zius-Global and vipul-zius and shellworlds/ZENVR
git push zius-global main:ZENVR72
git push vipul-zius main:ZENVR72
git push sw-z main:ZENVR72

# Push DENVR72 to dt-uk and muskan-dt and shellworlds/DENVR
git push dt-uk main:DENVR72
git push muskan-dt main:DENVR72
git push sw-d main:DENVR72

# Push QENVR72 to qb-eu and shellworlds/QENVR
git push qb-eu main:QENVR72
git push sw-q main:QENVR72

# Push AENVR72 to mike-aeq and shellworlds/AENVR
git push mike-aeq main:AENVR72
git push sw-a main:AENVR72

# Push main to shellworlds/ENVR
git push sw-envr main:main
```

## Collaborator mapping

- muskan-dt: dt-uk/DENVR (muskan.s@data-t.space)
- mike-aeq: shellworlds/AENVR (mike.s@a-eq.com)
- vipul-zius: shellworlds/ZENVR (vipul.j@zi-us.com)
