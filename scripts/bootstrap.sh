#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-dev}"

python3 scripts/config_validator.py --environment "$ENVIRONMENT" --generate

for project in cloudbudget infraflow netguardian netaegis; do
  if [[ -f "$project/scripts/setup.sh" ]]; then
    echo "[bootstrap] running $project setup"
    bash "$project/scripts/setup.sh"
  fi
  cp -n "$project/.env.example" "$project/.env" || true
done

echo "[bootstrap] complete for environment: $ENVIRONMENT"
