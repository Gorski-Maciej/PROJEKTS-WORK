#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "$ROOT/.env.example" && ! -f "$ROOT/.env" ]]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  echo "[infraflow] created .env from .env.example"
fi

if [[ -x "$ROOT/scripts/setup_keys.sh" ]]; then
  bash "$ROOT/scripts/setup_keys.sh"
fi

echo "[infraflow] setup complete"
