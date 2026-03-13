# SN-112BA

Unified quantum-cognitive architecture for contextual augmentation and biometric swarm intelligence. Main developer: shellworlds.

## Problem and Scope

See **INDEX.md** for problem statement and **POC_REPORT.md** for skillset, tools, What/Why/How/When. See **CLIENT_REPOS.md** for repo URLs and push commands.

## Install (one command)

**Lenovo (Ubuntu):**
```bash
cd /home/rrmr/Desktop/RRMR/BProjects/BorelSIgmaInc/SN112BA
chmod +x scripts/system_check.sh scripts/install_all.sh
./scripts/install_all.sh
```

**Mac:**
```bash
cd /path/to/SN112BA
chmod +x scripts/system_check.sh scripts/install_all.sh
./scripts/install_all.sh
```

**Windows** (WSL or Git Bash):
```bash
cd /path/to/SN112BA
bash scripts/install_all.sh
```

Uses pip (Python) and npm (Node) where available. Then run system check: `./scripts/system_check.sh` (or `bash scripts/system_check.sh` on Windows).

## Run

- System check: `./scripts/system_check.sh`
- Python: `pip install -r requirements.txt` then `python3 python/quantum_qft_20q.py`, `python3 python/fedstress_client.py`, `python3 python/pso_swarm.py`, `python3 python/kyber_sim.py`, `python3 python/biometric_signal.py`, `python3 python/graphs_2d_3d.py`
- API: `cd api && npm install && npm start` (port 3001)
- Dashboard: `cd dashboard && npm install && npm start` (Vite port 5173)
- Next: `cd next-app && npm install && npm run dev`
- Java: `cd java && javac BiometricProcessor.java && java BiometricProcessor`
- C++: `cd cpp && g++ -o swarm_node swarm_node.cpp && ./swarm_node`
- Go: `cd go/crypto && go run handshake.go`

## Branches (16)

main, ZENVR72, DENVR72, QENVR72, AENVR72, fedstress, quantum, swarm, crypto, api, dashboard, biometric, edge, watson, viz, release.

## Client pushes

See **CLIENT_REPOS.md** for remotes and copy-paste push commands to Zius-Global/ZENVR, dt-uk/DENVR, qb-eu/QENVR, vipul-zius/ZENVR, mike-aeq/AENVR, muskan-dt/DENVR and shellworlds backups.
