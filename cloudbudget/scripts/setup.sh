#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "$ROOT/.env.example" && ! -f "$ROOT/.env" ]]; then cp "$ROOT/.env.example" "$ROOT/.env"; echo "[cloudbudget] created .env from .env.example"; fi
echo "[cloudbudget] optional bootstrap commands:"
echo "  docker compose -f $ROOT/docker-compose.yml run --rm api python /app/scripts/init_duckdb.py"
echo "  docker compose -f $ROOT/docker-compose.yml run --rm api python /app/scripts/bootstrap_demo_data.py"
echo "[cloudbudget] setup complete"
