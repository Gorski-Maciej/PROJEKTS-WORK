#!/usr/bin/env bash
cp -n .env.example .env 2>/dev/null || true
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "$ROOT/.env.example" && ! -f "$ROOT/.env" ]]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  echo "[netguardian] created .env from .env.example"
fi

if [[ -x "$ROOT/scripts/setup_local_prereqs.sh" ]]; then
  bash "$ROOT/scripts/setup_local_prereqs.sh"
fi

echo "[netguardian] GeoIP reminder: add GeoLite2-City.mmdb to engine/data"
echo "[netguardian] setup complete"
