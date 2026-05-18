#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "_yy.txt"
FALLBACK_SOURCE = ROOT / "_nn.txt"
OUT = ROOT / "generated_project"
PROJECTS = ["cloudbudget", "infraflow", "netguardian", "netaegis"]
PORTS = {"cloudbudget": 9001, "infraflow": 9002, "netguardian": 9003, "netaegis": 9004}


def detect(text: str) -> list[str]:
    t = text.lower()
    return [p for p in PROJECTS if p in t]


def extract_actions(text: str) -> list[str]:
    rx = re.compile(r"\b(brak|dodaj|napraw|setup|docker compose|requirements\.txt|healthcheck|testy|makefile)\b", re.I)
    out = []
    for ln in (x.strip() for x in text.splitlines()):
        if len(ln) >= 10 and rx.search(ln):
            out.append(ln)
    dedup, seen = [], set()
    for x in out:
        if x not in seen:
            seen.add(x)
            dedup.append(x)
    return dedup[:200]


def classify(actions: list[str]) -> dict[str, list[str]]:
    grouped = {p: [] for p in PROJECTS}
    grouped["global"] = []
    for a in actions:
        l = a.lower()
        hit = False
        for p in PROJECTS:
            if p in l:
                grouped[p].append(a); hit = True
        if not hit:
            grouped["global"].append(a)
    return grouped


def write(path: Path, content: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if mode is not None:
        path.chmod(mode)


def build_service(project: str, port: int, actions: list[str]) -> None:
    base = OUT / project
    write(base / ".env.example", f"PROJECT_NAME={project}\nPROJECT_PORT=8000\n")
    write(base / "requirements.txt", "fastapi==0.115.0\nuvicorn==0.30.6\npydantic==2.9.2\npytest==8.3.3\nhttpx==0.27.2\n")
    write(base / "app" / "main.py", (
        "from fastapi import FastAPI\nfrom pydantic import BaseModel\n\n"
        f"ACTIONS = {actions!r}\n"
        f"app = FastAPI(title=\"{project}\")\n\n"
        "class Action(BaseModel):\n    text: str\n\n"
        "@app.get('/health')\ndef health():\n    return {'status': 'ok', 'project': app.title}\n\n"
        "@app.get('/actions')\ndef list_actions():\n    return {'project': app.title, 'actions': ACTIONS}\n\n"
        "@app.post('/actions')\ndef add_action(item: Action):\n    return {'project': app.title, 'accepted': item.text}\n"
    ))
    write(base / "tests" / "test_app.py", (
        "from fastapi.testclient import TestClient\nfrom app.main import app\n\n"
        "client = TestClient(app)\n\n"
        "def test_health():\n    r = client.get('/health')\n    assert r.status_code == 200\n    assert r.json()['status'] == 'ok'\n\n"
        "def test_actions():\n    r = client.get('/actions')\n    assert r.status_code == 200\n    assert 'actions' in r.json()\n"
    ))
    write(base / "Dockerfile", (
        "FROM python:3.11-slim\nWORKDIR /app\n"
        "COPY requirements.txt /app/requirements.txt\nRUN pip install --no-cache-dir -r /app/requirements.txt\n"
        "COPY app /app/app\nCOPY tests /app/tests\n"
        "CMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n"
    ))
    write(base / "README.md", f"# {project}\nGenerated runnable FastAPI service. Exposed on localhost:{port}.\n")


def build_root(meta: dict) -> None:
    lines = ["services:"]
    for p in PROJECTS:
        lines += [f"  {p}:", f"    build: ./{p}", f"    env_file: ./{p}/.env.example", "    ports:", f"      - \"{PORTS[p]}:8000\"", "    healthcheck:", "      test: [\"CMD\", \"python\", \"-c\", \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)\"]", "      interval: 15s", "      timeout: 5s", "      retries: 5"]
    write(OUT / "docker-compose.yml", "\n".join(lines) + "\n")
    write(OUT / "README.md", "# Generated Project from _nn.txt\n\n## Start\n```bash\n./setup.sh\n./run_all.sh\n```\n\n## Tests\n```bash\n./test_all.sh\n```\n\n## Smoke check\n```bash\n./run_all.sh\ncurl http://localhost:9001/summary\n```\n")
    write(OUT / "setup.sh", "#!/usr/bin/env bash\nset -euo pipefail\nfor p in cloudbudget infraflow netguardian netaegis; do cp -n \"$p/.env.example\" \"$p/.env\" || true; done\n", 0o755)
    write(OUT / "run_all.sh", "#!/usr/bin/env bash\nset -euo pipefail\ndocker compose up -d --build\n", 0o755)
    write(OUT / "stop_all.sh", "#!/usr/bin/env bash\nset -euo pipefail\ndocker compose down --remove-orphans\n", 0o755)
    write(OUT / "test_all.sh", "#!/usr/bin/env bash\nset -euo pipefail\nfor p in cloudbudget infraflow netguardian netaegis; do docker compose run --rm $p pytest -q; done\n", 0o755)
    write(OUT / "NN_BUILD.json", json.dumps(meta, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=None, help="source guidance file (default: _yy.txt, fallback: _nn.txt)")
    args = ap.parse_args()
    src = Path(args.source) if args.source else (DEFAULT_SOURCE if DEFAULT_SOURCE.exists() else FALLBACK_SOURCE)
    text = src.read_text(encoding="utf-8", errors="replace") if src.exists() else ""
    fp = hashlib.sha256(text.encode()).hexdigest()[:12] if text else "unknown"
    found = detect(text)
    grouped = classify(extract_actions(text))
    for p in PROJECTS:
        build_service(p, PORTS[p], grouped.get(p, []) + grouped.get("global", []))
    meta = {"source_file": str(src.name), "fingerprint": fp, "detected_projects": found, "generated_projects": PROJECTS, "ports": PORTS, "actions_by_project": grouped}
    build_root(meta)
    print(f"generated_project built with runnable services (fingerprint={fp})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
