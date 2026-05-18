#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT/scripts/demo_projects.sh"
command -v docker >/dev/null 2>&1 || { echo "docker command not found" >&2; exit 1; }
if [[ "${1:-}" == "--with-setup" ]]; then
  "$ROOT/setup.sh"
fi
start_project(){ local name="$1" dir="$2" override="$3"; printf '\n=== [%s] starting ===\n' "$name"; if [[ -n "$override" ]]; then (cd "$ROOT/$dir" && docker compose -f docker-compose.yml -f "$override" up -d --build); else (cd "$ROOT/$dir" && docker compose up -d --build); fi; }
for entry in "${DEMO_PROJECTS[@]}"; do IFS='|' read -r name dir override _ <<< "$entry"; start_project "$name" "$dir" "$override"; done
printf '\nAll demo environments are running.\n'; printf 'CloudBudget frontend:      http://localhost:3000\nCloudBudget API docs:      http://localhost:8000/docs\nInfraFlow dashboard:       http://localhost:8180\nInfraFlow API docs:        http://localhost:8100/docs\nNetGuardian dashboard:     http://localhost:8280\nNetGuardian API docs:      http://localhost:8200/docs\nNetAegis frontend:         http://localhost:3300\nNetAegis Main MCP docs:    http://localhost:8300/docs\nNetAegis Operational docs: http://localhost:8301/docs\n'
