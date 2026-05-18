#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/tools/demo_projects.sh"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1"; return 1; }
}

check_env_example() {
  local dir="$1"
  [[ -f "$ROOT/$dir/.env.example" ]] || { echo "[$dir] missing .env.example"; return 1; }
}

check_setup_script() {
  local dir="$1" setup_rel="$2"
  [[ -n "$setup_rel" && -x "$ROOT/$dir/$setup_rel" ]] || { echo "[$dir] setup script missing/not executable: $setup_rel"; return 1; }
}

check_compose_config() {
  local dir="$1" override="$2"
  if [[ -n "$override" ]]; then
    (cd "$ROOT/$dir" && docker compose -f docker-compose.yml -f "$override" config >/dev/null)
  else
    (cd "$ROOT/$dir" && docker compose config >/dev/null)
  fi
}

main() {
  local failed=0
  require_cmd docker || failed=1

  for entry in "${DEMO_PROJECTS[@]}"; do
    IFS='|' read -r name dir override setup_rel <<< "$entry"
    echo "== checking $name ($dir) =="
    check_env_example "$dir" || failed=1
    check_setup_script "$dir" "$setup_rel" || failed=1
    check_compose_config "$dir" "$override" || { echo "[$dir] compose config invalid"; failed=1; }
  done

  if [[ $failed -ne 0 ]]; then
    echo "Demo doctor: FAILED"
    exit 1
  fi
  echo "Demo doctor: OK"
}

main "$@"
