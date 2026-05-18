#!/usr/bin/env bash
set -euo pipefail
python -m py_compile tools/nn_build_project.py
python tools/nn_build_project.py --source _nn.txt >/tmp/nn_build.out
rg "generated_project built with runnable services" /tmp/nn_build.out >/dev/null
test -f generated_project/docker-compose.yml
test -f generated_project/cloudbudget/app/main.py
test -f generated_project/cloudbudget/tests/test_app.py
test -f generated_project/test_all.sh
rg "healthcheck" generated_project/docker-compose.yml >/dev/null
rg "actions_by_project" generated_project/NN_BUILD.json >/dev/null
