#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATUS=0

check_file() {
  local file="$1"
  local label="$2"
  if [[ -f "${file}" ]]; then
    echo "[OK] ${label}: ${file}"
  else
    echo "[MISSING] ${label}: ${file}"
    STATUS=1
  fi
}

check_file "${ROOT_DIR}/agent/authorized_keys" "SSH authorized keys"
check_file "${ROOT_DIR}/engine/ssh/id_rsa" "Engine private SSH key"
check_file "${ROOT_DIR}/engine/data/GeoLite2-City.mmdb" "GeoIP database"

if [[ -f "${ROOT_DIR}/.env" ]]; then
  echo "[OK] Environment file: ${ROOT_DIR}/.env"
else
  echo "[WARN] Environment file missing: ${ROOT_DIR}/.env (copy from .env.example)"
fi

if [[ ${STATUS} -ne 0 ]]; then
  echo "\nOne or more required files are missing. Run ./scripts/setup_local_prereqs.sh and add GeoLite2 DB."
fi

exit ${STATUS}
