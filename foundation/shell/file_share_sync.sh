#!/usr/bin/env bash
set -euo pipefail
SRC=${1:-./shared}
DST=${2:-./mirror}
mkdir -p "$SRC" "$DST"
rsync -av --delete "$SRC/" "$DST/"
