#!/usr/bin/env python3
"""Validate project .env.example files against docker-compose variable usage."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECTS = ("cloudbudget", "infraflow", "netguardian", "netaegis")
VAR_RE = re.compile(r"\$\{([A-Z0-9_]+)(?::-[^}]*)?}")
ENV_KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def compose_vars(text: str) -> set[str]:
    return set(VAR_RE.findall(text))


def parse_env_example(text: str) -> tuple[set[str], list[str], list[str]]:
    keys: set[str] = set()
    duplicates: list[str] = []
    malformed: list[str] = []

    for idx, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            malformed.append(f"line {idx}: missing '=' -> {raw}")
            continue
        key = line.split("=", 1)[0].strip()
        if not ENV_KEY_RE.match(key):
            malformed.append(f"line {idx}: invalid key '{key}'")
            continue
        if key in keys:
            duplicates.append(key)
        keys.add(key)

    return keys, sorted(set(duplicates)), malformed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projects", nargs="*", default=list(DEFAULT_PROJECTS))
    args = parser.parse_args()

    failures: list[str] = []
    for project in args.projects:
        compose_path = ROOT / project / "docker-compose.yml"
        env_example_path = ROOT / project / ".env.example"
        if not compose_path.exists() or not env_example_path.exists():
            failures.append(f"{project}: missing docker-compose.yml or .env.example")
            continue

        compose = compose_path.read_text(encoding="utf-8")
        keys, duplicates, malformed = parse_env_example(env_example_path.read_text(encoding="utf-8"))
        required = compose_vars(compose)

        missing = sorted(v for v in required if v not in keys)
        if missing:
            failures.append(f"{project}: missing in .env.example -> {', '.join(missing)}")
        if duplicates:
            failures.append(f"{project}: duplicate keys -> {', '.join(duplicates)}")
        if malformed:
            failures.append(f"{project}: malformed lines -> {'; '.join(malformed)}")

    if failures:
        print("ENV validation failed:")
        for f in failures:
            print(f" - {f}")
        return 1

    print("All project .env.example files cover docker-compose interpolated variables and pass syntax checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
