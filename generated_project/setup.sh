#!/usr/bin/env bash
set -euo pipefail
for p in cloudbudget infraflow netguardian netaegis; do cp -n "$p/.env.example" "$p/.env" || true; done
