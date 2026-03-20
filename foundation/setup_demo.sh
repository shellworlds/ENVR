#!/usr/bin/env bash
set -euo pipefail
python3 foundation/python/quantum_sim.py
node foundation/node/cluster_manager.js
go run foundation/go/node_discovery.go
bash foundation/shell/system_check.sh foundation/system_report.txt
echo "Demo complete"
