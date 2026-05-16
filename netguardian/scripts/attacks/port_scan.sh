#!/usr/bin/env bash
set -euo pipefail

TARGET_HOST="${1:-engine}"
PORT_RANGE="${2:-1-100}"

echo "[netguardian] Starting TCP SYN port scan against ${TARGET_HOST}, ports ${PORT_RANGE}"
exec nmap -sS -p "${PORT_RANGE}" "${TARGET_HOST}"
