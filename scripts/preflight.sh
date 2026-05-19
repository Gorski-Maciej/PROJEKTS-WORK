#!/bin/bash
echo "=== Pre-flight checks ==="
docker info > /dev/null 2>&1 || { echo "Docker not running"; exit 1; }
./verify_all_ports.sh || { echo "Port conflicts found"; exit 1; }
python3 scripts/config_validator.py || { echo "Config validation failed"; exit 1; }
echo "All checks passed"
