#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "${ROOT_DIR}/engine/ssh" "${ROOT_DIR}/engine/data" "${ROOT_DIR}/agent"

if [[ ! -f "${ROOT_DIR}/engine/ssh/id_rsa" ]]; then
  ssh-keygen -t rsa -b 4096 -f "${ROOT_DIR}/engine/ssh/id_rsa" -N ""
fi

cp "${ROOT_DIR}/engine/ssh/id_rsa.pub" "${ROOT_DIR}/agent/authorized_keys"
chmod 600 "${ROOT_DIR}/engine/ssh/id_rsa"
chmod 644 "${ROOT_DIR}/engine/ssh/id_rsa.pub" "${ROOT_DIR}/agent/authorized_keys"

echo "[netguardian] SSH keys ready."
echo "[netguardian] Place GeoLite DB manually at: ${ROOT_DIR}/engine/data/GeoLite2-City.mmdb"
