#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "_yy.txt"
FALLBACK_SOURCE = ROOT / "_nn.txt"
KNOWN_PROJECTS = ("cloudbudget", "infraflow", "netguardian", "netaegis")
MANAGED_MARKER = "# managed-by: tools/generate_from_nn.py"

@dataclass(frozen=True)
class FileSpec:
    path: str
    content: str
    executable: bool = False


def detect_projects_from_nn(nn_text: str) -> list[str]:
    lower = nn_text.lower()
    return [p for p in KNOWN_PROJECTS if p in lower]


def extract_actionable_lines(nn_text: str) -> list[str]:
    rx = re.compile(r"\b(brak|dodaj|napraw|setup|docker compose|requirements\.txt|healthcheck|testy|makefile)\b", re.I)
    out = []
    for ln in (x.strip() for x in nn_text.splitlines()):
        if len(ln) >= 10 and rx.search(ln):
            out.append(ln)
    dedup, seen = [], set()
    for ln in out:
        if ln not in seen:
            seen.add(ln)
            dedup.append(ln)
    return dedup[:200]


def classify_actions(actions: list[str]) -> dict[str, list[str]]:
    grouped = {p: [] for p in KNOWN_PROJECTS}
    grouped["global"] = []
    for a in actions:
        lower = a.lower()
        matched = False
        for p in KNOWN_PROJECTS:
            if p in lower:
                grouped[p].append(a)
                matched = True
        if not matched:
            grouped["global"].append(a)
    return grouped


def script_header() -> str:
    return f"#!/usr/bin/env bash\nset -euo pipefail\n{MANAGED_MARKER}\n"


def build_specs(nn_text: str) -> list[FileSpec]:
    detected = detect_projects_from_nn(nn_text)
    actions = extract_actionable_lines(nn_text)
    grouped = classify_actions(actions)
    nn_hash = hashlib.sha256(nn_text.encode()).hexdigest()[:12] if nn_text else "unknown"

    nn_tasks = {"source_fingerprint": nn_hash, "detected_projects": detected, "actions_by_project": grouped}
    specs = [
        FileSpec("NN_TASKS.json", json.dumps(nn_tasks, ensure_ascii=False, indent=2) + "\n"),
        FileSpec("RUN_DEMO.md", f"# Demo quickstart generated from _nn.txt\n\nSource fingerprint: `{nn_hash}`\n\n1. `make demo-check`\n2. `make generate-from-nn`\n3. `make demo-start`\n4. `make demo-stop`\n\n{MANAGED_MARKER}\n"),
        FileSpec("NN_GENERATED_CHECKLIST.md", "# NN_GENERATED_CHECKLIST\n\n" + "\n".join([f"- `{p}`: {'present' if p in detected else 'missing in _nn.txt'}" for p in KNOWN_PROJECTS]) + f"\n\n{MANAGED_MARKER}\n"),
        FileSpec("NN_IMPLEMENTATION_GUIDE.md", "# NN_IMPLEMENTATION_GUIDE\n\n" + "\n".join([f"- {x}" for x in actions]) + f"\n\n{MANAGED_MARKER}\n"),
    ]

    for proj in KNOWN_PROJECTS:
        lines = grouped.get(proj, []) + grouped.get("global", [])
        content = (
            f"# {proj.upper()}_IMPLEMENTATION_PLAN\n\n"
            f"Source fingerprint: `{nn_hash}`\n\n"
            "## Action backlog from _nn.txt\n\n"
            + "\n".join(f"- [ ] {ln}" for ln in (lines or ["Brak wykrytych zadań dla projektu"]))
            + f"\n\n{MANAGED_MARKER}\n"
        )
        specs.append(FileSpec(f"{proj}/NN_IMPLEMENTATION_PLAN.md", content))

    scripts = {
        "cloudbudget/scripts/setup_local_demo.sh": "cp -n \"$ROOT/.env.example\" \"$ROOT/.env\" || true\n",
        "infraflow/scripts/setup_local_demo.sh": "cp -n \"$ROOT/.env.example\" \"$ROOT/.env\" || true\nbash \"$ROOT/scripts/setup_keys.sh\"\n",
        "netguardian/scripts/setup_local_demo.sh": "cp -n \"$ROOT/.env.example\" \"$ROOT/.env\" || true\nbash \"$ROOT/scripts/setup_local_prereqs.sh\"\n",
        "netaegis/scripts/setup_local_demo.sh": "cp -n \"$ROOT/.env.example\" \"$ROOT/.env\" || true\n",
    }
    for path, body in scripts.items():
        specs.append(FileSpec(path, script_header() + "ROOT=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)\"\n" + body, True))
    return specs


def should_write(path: Path, sync: bool) -> bool:
    if not path.exists():
        return True
    if not sync:
        return False
    return MANAGED_MARKER in path.read_text(encoding="utf-8", errors="replace") or path.name == "NN_TASKS.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sync", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--source", default=None, help="source guidance file (default: _yy.txt, fallback: _nn.txt)")
    args = ap.parse_args()

    src = Path(args.source) if args.source else (DEFAULT_SOURCE if DEFAULT_SOURCE.exists() else FALLBACK_SOURCE)
    nn_text = src.read_text(encoding="utf-8", errors="replace") if src.exists() else ""
    specs = build_specs(nn_text)
    changed, skipped, protected = [], [], []
    for s in specs:
        p = ROOT / s.path
        if not should_write(p, args.sync):
            (protected if p.exists() and args.sync else skipped).append(s.path)
            continue
        changed.append(s.path)
        if args.dry_run:
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(s.content, encoding="utf-8")
        if s.executable:
            p.chmod(0o755)

    print(f"Mode: {'DRY-RUN' if args.dry_run else 'WRITE'}")
    print("Changed:")
    print("\n".join([f"  - {x}" for x in changed]) or "  - (none)")
    print("Skipped:")
    print("\n".join([f"  - {x}" for x in skipped]) or "  - (none)")
    if protected:
        print("Protected:")
        print("\n".join([f"  - {x}" for x in protected]))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
