import json
import subprocess

from scripts.audit_projects import run_audit


def test_audit_projects_current_repo_state_is_valid():
    report = run_audit()
    assert report["ok"] is True
    assert report["missing"] == []
    assert report["empty"] == []


def test_audit_projects_json_mode_outputs_valid_schema():
    completed = subprocess.run(
        ["python", "scripts/audit_projects.py", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert set(payload.keys()) == {"ok", "missing", "empty"}
    assert isinstance(payload["ok"], bool)
    assert isinstance(payload["missing"], list)
    assert isinstance(payload["empty"], list)
