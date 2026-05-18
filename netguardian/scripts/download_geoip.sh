#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NETGUARDIAN_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_DIR="${NETGUARDIAN_DIR}/engine/data"
TARGET_FILE="${TARGET_DIR}/GeoLite2-City.mmdb"

mkdir -p "${TARGET_DIR}"

cat <<MSG
Pobierz plik GeoLite2-City.mmdb z https://www.maxmind.com.
Aby zapisać plik do projektu uruchom:
  $0 /sciezka/do/GeoLite2-City.mmdb

Docelowa ścieżka zapisu:
${TARGET_FILE}
MSG

if [[ $# -ne 1 ]]; then
  echo "Użycie: $0 /sciezka/do/GeoLite2-City.mmdb" >&2
  exit 1
fi

SOURCE_FILE="$1"
if [[ ! -f "${SOURCE_FILE}" ]]; then
  echo "Błąd: nie znaleziono pliku źródłowego: ${SOURCE_FILE}" >&2
  exit 1
fi

cp "${SOURCE_FILE}" "${TARGET_FILE}"
echo "Zapisano plik do: ${TARGET_FILE}"
