#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT/scripts/demo_projects.sh"
stop_project(){ local name="$1" dir="$2" override="$3"; printf '\n=== [%s] stopping ===\n' "$name"; if [[ -n "$override" ]]; then (cd "$ROOT/$dir" && docker compose -f docker-compose.yml -f "$override" down --remove-orphans); else (cd "$ROOT/$dir" && docker compose down --remove-orphans); fi; }
for entry in "${DEMO_PROJECTS[@]}"; do IFS='|' read -r name dir override _ <<< "$entry"; stop_project "$name" "$dir" "$override"; done
printf '\nAll demo environments are stopped.\n'
