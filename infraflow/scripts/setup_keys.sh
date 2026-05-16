#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KEY_PATH="${ROOT_DIR}/keys/id_rsa"
mkdir -p "${ROOT_DIR}/keys"
if [[ -f "${KEY_PATH}" ]]; then
  echo "SSH key already exists: ${KEY_PATH}"
  exit 0
fi
ssh-keygen -t rsa -b 4096 -N "" -f "${KEY_PATH}"
echo "Generated SSH keypair at ${KEY_PATH} and ${KEY_PATH}.pub"
