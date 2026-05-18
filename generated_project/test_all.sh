#!/usr/bin/env bash
set -euo pipefail
for p in cloudbudget infraflow netguardian netaegis; do docker compose run --rm $p pytest -q; done
