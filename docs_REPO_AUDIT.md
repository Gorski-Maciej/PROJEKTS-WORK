# Repository Audit & Validation Guide

This repository includes automated checks derived from:
`wed_may_20_2026_project_audit_and_code_generation_plan (1).md`.

## Local commands

- Validate environment examples:

```bash
make validate-env
```

- Run repository structural audit:

```bash
make audit
```

- Run full repository audit bundle (without tests):

```bash
make check
```

## What is covered

### `scripts/validate_env_examples.py`
- Ensures `.env.example` exists for each project.
- Ensures `${VAR}` and `${VAR:-default}` used in `docker-compose.yml` are present.
- Checks env key syntax and duplicate keys.

### `scripts/audit_projects.py`
- Verifies required Dockerfiles/config files exist.
- Verifies key service entrypoints exist and are non-empty.
- Supports machine-readable output:

```bash
python scripts/audit_projects.py --json
```

## CI

GitHub Actions workflow:
- `.github/workflows/repo-audit.yml`

Runs on PR and push to `main` and executes:
1. `make validate-env`
2. `make audit`
3. `make verify-ports`
