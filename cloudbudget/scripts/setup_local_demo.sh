#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cp -n "$ROOT/.env.example" "$ROOT/.env" || true
echo "[cloudbudget] optionally run: docker compose run --rm api python /app/scripts/init_duckdb.py"
echo "[cloudbudget] optionally run: docker compose run --rm api python /app/scripts/bootstrap_demo_data.py"
