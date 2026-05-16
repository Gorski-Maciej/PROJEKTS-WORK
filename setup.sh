#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp -n "$ROOT/infraflow/.env.example" "$ROOT/infraflow/.env" || true
cp -n "$ROOT/netguardian/.env.example" "$ROOT/netguardian/.env" || true

bash "$ROOT/infraflow/scripts/setup_keys.sh"
if [[ -x "$ROOT/netguardian/scripts/setup_local_prereqs.sh" ]]; then
  bash "$ROOT/netguardian/scripts/setup_local_prereqs.sh"
fi

echo "Setup complete. Add GeoLite2-City.mmdb to netguardian/engine/data/ before full run."
