#!/usr/bin/env python3
"""Static audit checks for PROJEKTS-WORK based on Wed May 20 2026 plan."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "infraflow/engine/Dockerfile",
    "netguardian/engine/Dockerfile",
    "netguardian/agent/Dockerfile",
    "netguardian/dashboard/Dockerfile",
    "netaegis/agents/seclog/Dockerfile",
    "netaegis/agents/netconfig/Dockerfile",
    "netaegis/frontend/Dockerfile",
    "infraflow/prometheus/prometheus.yml",
    "netguardian/prometheus/prometheus.yml",
    "infraflow/grafana/provisioning/datasources/datasource.yml",
    "infraflow/grafana/provisioning/dashboards/dashboard.yml",
    "netguardian/grafana/provisioning/datasources/prometheus.yml",
    "netguardian/grafana/provisioning/dashboards/dashboards.yml",
    "cloudbudget/.env.example",
    "infraflow/.env.example",
    "netguardian/.env.example",
    "netaegis/.env.example",
]

KEY_ENTRYPOINTS = [
    "cloudbudget/api/main.py",
    "infraflow/engine/main.py",
    "netguardian/engine/main.py",
    "netguardian/agent/agent.py",
    "netaegis/server/main_mcp/main.py",
    "netaegis/server/operational_mcp/main.py",
    "netaegis/agents/seclog/main.py",
    "netaegis/agents/netconfig/main.py",
    "netaegis/agents/netpulse/main.py",
]


def run_audit() -> dict:
    missing: list[str] = []
    empty: list[str] = []

    for rel in REQUIRED_FILES:
        p = ROOT / rel
        if not p.exists():
            missing.append(rel)

    for rel in KEY_ENTRYPOINTS:
        p = ROOT / rel
        if not p.exists():
            missing.append(rel)
        elif p.stat().st_size == 0:
            empty.append(rel)

    return {
        "ok": not (missing or empty),
        "missing": sorted(set(missing)),
        "empty": sorted(empty),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON report")
    args = parser.parse_args()

    report = run_audit()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        if report["ok"]:
            print("Project audit checks passed (required files and entrypoints exist).")
        else:
            print("Project audit checks failed.")
            if report["missing"]:
                print("Missing required files:")
                for item in report["missing"]:
                    print(f" - {item}")
            if report["empty"]:
                print("Empty key entrypoints:")
                for item in report["empty"]:
                    print(f" - {item}")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
