#!/usr/bin/env sh
set -eu
if [ "${SKIP_GEOIP_CHECK:-true}" = "true" ]; then
  echo "Skipping GeoIP checks for demo mode"
  exit 0
fi
if [ ! -f "${GEOIP_DB:-/app/data/GeoLite2-City.mmdb}" ]; then
  echo "GeoIP DB missing at ${GEOIP_DB:-/app/data/GeoLite2-City.mmdb}"
  exit 1
fi
