#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cp -n "$ROOT/.env.example" "$ROOT/.env" || true
bash "$ROOT/scripts/setup_keys.sh"
