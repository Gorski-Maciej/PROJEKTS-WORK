#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cp -n "$ROOT/.env.example" "$ROOT/.env" || true
bash "$ROOT/scripts/setup_local_prereqs.sh"
echo "[netguardian] GeoIP file required: engine/data/GeoLite2-City.mmdb"
