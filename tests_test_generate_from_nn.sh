#!/usr/bin/env bash
set -euo pipefail
python -m py_compile tools/generate_from_nn.py
python tools/generate_from_nn.py --dry-run --source _nn.txt >/tmp/generator.out
rg "Mode: DRY-RUN|Changed:|Skipped:" /tmp/generator.out >/dev/null
python tools/generate_from_nn.py --sync --source _nn.txt >/tmp/generator_sync.out
rg "Mode: WRITE|Changed:|Skipped:" /tmp/generator_sync.out >/dev/null
python - <<'PY'
import json
from pathlib import Path
from tools.generate_from_nn import detect_projects_from_nn, extract_actionable_lines, classify_actions
text='cloudbudget infraflow netguardian netaegis\nDodaj setup\nBrak requirements.txt\nNetGuardian brak healthcheck'
assert detect_projects_from_nn(text)==['cloudbudget','infraflow','netguardian','netaegis']
actions=extract_actionable_lines(text)
assert any('Brak requirements.txt' in a for a in actions)
g=classify_actions(actions)
assert 'global' in g and 'netguardian' in g
print('ok')
print(Path('NN_TASKS.json').exists())
PY
