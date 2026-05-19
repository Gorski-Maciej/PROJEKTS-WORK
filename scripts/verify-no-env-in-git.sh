#!/usr/bin/env sh
set -eu
tracked=$(git ls-files | grep -E "(^|/)\.env$" || true)
if [ -n "$tracked" ]; then
  echo "Tracked .env files detected:"
  echo "$tracked"
  exit 1
fi
echo "No tracked .env files found."
