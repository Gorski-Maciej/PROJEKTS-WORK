#!/usr/bin/env bash
set -euo pipefail

PROJECTS=(cloudbudget infraflow netguardian netaegis)
FILES=()

for project in "${PROJECTS[@]}"; do
  compose_file="$project/docker-compose.yml"
  if [[ -f "$compose_file" ]]; then
    FILES+=("$compose_file")
  else
    echo "[WARN] Brak pliku: $compose_file"
  fi
done

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "[ERROR] Nie znaleziono plików docker-compose.yml do analizy"
  exit 1
fi

python3 - "${FILES[@]}" <<'PY'
import re
import sys
from collections import defaultdict

files = sys.argv[1:]
map_re = re.compile(r'(?P<host>\d{2,5}):(?P<container>\d{2,5})(?:/(?P<proto>tcp|udp))?$')
inline_ports_re = re.compile(r'\bports\s*:\s*\[(?P<vals>[^\]]*)\]')

records = []

for file in files:
    with open(file, encoding='utf-8') as fh:
        lines = fh.readlines()

    in_ports_block = False
    ports_indent = 0

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip('\n')
        stripped = line.strip()

        # Obsługa formatu inline: ports: ["8100:8000", "15673:15672"]
        inline = inline_ports_re.search(line)
        if inline:
            values = [v.strip().strip('"\'') for v in inline.group('vals').split(',') if v.strip()]
            for value in values:
                m = map_re.match(value)
                if m:
                    proto = m.group('proto') or 'tcp'
                    records.append((int(m.group('host')), int(m.group('container')), proto, file, lineno, value))
            continue

        # Wejście w blok ports:
        if re.match(r'^\s*ports\s*:\s*$', line):
            in_ports_block = True
            ports_indent = len(line) - len(line.lstrip(' '))
            continue

        if in_ports_block:
            current_indent = len(line) - len(line.lstrip(' '))

            # Koniec bloku (mniejszy/equal indent i nie jest to element listy)
            if stripped and current_indent <= ports_indent and not stripped.startswith('-'):
                in_ports_block = False
                continue

            # Element listy: - "8100:8000"
            item_match = re.match(r'^\s*-\s*(.+?)\s*$', line)
            if item_match:
                value = item_match.group(1).strip().strip('"\'')
                m = map_re.match(value)
                if m:
                    proto = m.group('proto') or 'tcp'
                    records.append((int(m.group('host')), int(m.group('container')), proto, file, lineno, value))

by_host_port = defaultdict(list)
for host, container, proto, file, lineno, raw in records:
    by_host_port[(host, proto)].append((container, file, lineno, raw))

print('=== RAPORT PORTÓW (host -> kontener) ===')
if not records:
    print('Brak mapowań portów host:container w analizowanych plikach.')
else:
    for host, proto in sorted(by_host_port.keys()):
        for container, file, lineno, raw in sorted(by_host_port[(host, proto)], key=lambda x: (x[1], x[2])):
            print(f'{host}/{proto} -> {container}    [{file}:{lineno}] ({raw})')

print('\n=== WERYFIKACJA UNIKALNOŚCI ===')
conflicts = {key: vals for key, vals in by_host_port.items() if len(vals) > 1}
if conflicts:
    print('KONFLIKTY WYKRYTE:')
    for (host, proto), vals in sorted(conflicts.items()):
        print(f'- Port {host}/{proto} występuje {len(vals)} razy:')
        for container, file, lineno, raw in sorted(vals, key=lambda x: (x[1], x[2])):
            print(f'  * {file}:{lineno} ({raw})')
    sys.exit(2)

print('OK: wszystkie porty hosta są unikalne.')
PY
