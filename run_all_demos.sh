#!/bin/bash
echo "=== Uruchamianie wszystkich 4 projektów ==="
for proj in cloudbudget infraflow netguardian netaegis; do
  echo "--- $proj ---"
  cd $proj
  bash scripts/setup.sh
  cd ..
done
echo "=== Wszystkie systemy gotowe ==="
echo "CloudBudget: http://localhost:3100 | API: http://localhost:8100/docs"
echo "InfraFlow:   http://localhost:8081 | API: http://localhost:8001/docs"
echo "NetGuardian: http://localhost:8301 | API: http://localhost:8300/docs"
echo "NetAegis:    http://localhost:3400 | API: http://localhost:8400/docs"
