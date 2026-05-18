#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT/scripts/demo_projects.sh"
run_project_setup(){ local name="$1" dir="$2" setup_rel="$3"; local script_path="$ROOT/$dir/$setup_rel"; printf '\n=== [%s] setup ===\n' "$name"; if [[ -n "$setup_rel" && -x "$script_path" ]]; then bash "$script_path"; else printf '[%s] no executable setup script found (%s), skipped\n' "$name" "$setup_rel"; fi; }
for entry in "${DEMO_PROJECTS[@]}"; do IFS='|' read -r name dir _ setup_rel <<< "$entry"; run_project_setup "$name" "$dir" "$setup_rel"; done
printf '\nGlobal setup complete.\n'; printf 'Next: ./run_all_demos.sh\n'
