#!/usr/bin/env bash
set -euo pipefail
cp -n .env.example .env 2>/dev/null || true

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "$ROOT/.env.example" && ! -f "$ROOT/.env" ]]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  echo "[netguardian] created .env from .env.example"
fi

if [[ -x "$ROOT/scripts/setup_local_prereqs.sh" ]]; then
  bash "$ROOT/scripts/setup_local_prereqs.sh"
fi

# JWT_SECRET validation (if defined)
if [[ -f "$ROOT/.env" ]] && grep -q '^JWT_SECRET=' "$ROOT/.env"; then
  jwt_secret=$(sed -n 's/^JWT_SECRET=//p' "$ROOT/.env" | head -n1 | tr -d '[:space:]' | tr -d '"' | tr -d "'")
  case "${jwt_secret,,}" in
    ""|demo|default|change-me|change_me|please-change|replace-me|replace_me|local_dev_jwt_secret_replace_me_32chars_min|cloudbudget_local_jwt_secret_please_change|infraflow_local_jwt_secret_please_change)
      echo "[netguardian] ERROR: JWT_SECRET in .env must be set to a non-default value."
      exit 1
      ;;
  esac
fi

echo "[netguardian] GeoIP reminder: add GeoLite2-City.mmdb to engine/data"
echo "[netguardian] setup complete"

command -v docker >/dev/null || { echo "Docker not found"; exit 1; }
docker compose -f "$ROOT/docker-compose.yml" up -d --build
