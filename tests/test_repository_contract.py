from pathlib import Path


def _must_exist(path: str) -> None:
    assert Path(path).exists(), f"Missing required file: {path}"


def _must_contain(path: str, needle: str) -> None:
    content = Path(path).read_text(encoding="utf-8")
    assert needle in content, f"Expected '{needle}' in {path}"


def _read(path: str) -> str:
    _must_exist(path)
    return Path(path).read_text(encoding="utf-8")


def test_monitoring_files_exist():
    required = [
        "infraflow/prometheus/prometheus.yml",
        "infraflow/grafana/provisioning/datasources/datasource.yml",
        "infraflow/grafana/provisioning/dashboards/dashboard.yml",
        "netguardian/prometheus/prometheus.yml",
        "netguardian/grafana/provisioning/datasources/prometheus.yml",
        "netguardian/grafana/provisioning/dashboards/dashboards.yml",
    ]
    for path in required:
        _must_exist(path)


def test_setup_scripts_exist():
    for path in [
        "cloudbudget/scripts/setup.sh",
        "infraflow/scripts/setup.sh",
        "netguardian/scripts/setup.sh",
        "netaegis/scripts/setup.sh",
    ]:
        _must_exist(path)


def test_dependency_manifests_exist_and_not_empty():
    for path in [
        "cloudbudget/requirements.txt",
        "infraflow/requirements.txt",
        "netguardian/requirements.txt",
        "cloudbudget/pyproject.toml",
        "infraflow/pyproject.toml",
        "netguardian/pyproject.toml",
    ]:
        _must_exist(path)
        assert Path(path).read_text(encoding="utf-8").strip(), f"File is empty: {path}"


def test_env_examples_have_required_keys():
    checks = {
        "cloudbudget/.env.example": ["DATABASE_URL=", "REDIS_URL=", "RABBITMQ_URL=", "JWT_SECRET="],
        "infraflow/.env.example": ["DATABASE_URL=", "REDIS_HOST=", "CONFIG_PATH=", "JWT_SECRET="],
        "netguardian/.env.example": ["DATABASE_URL=", "KAFKA_BOOTSTRAP_SERVERS=", "REDIS_HOST=", "JWT_SECRET="],
        "netaegis/.env.example": ["MAIN_MCP_URL=", "OPERATIONAL_MCP_URL=", "NETCONFIG_DEVICE_USERNAME="],
    }
    for path, keys in checks.items():
        content = _read(path)
        for key in keys:
            assert key in content, f"Missing env key '{key}' in {path}"


def test_cloudbudget_compose_has_persistent_volumes():
    compose = "cloudbudget/docker-compose.yml"
    _must_contain(compose, "postgres_data:/var/lib/postgresql/data")
    _must_contain(compose, "rabbitmq_data:/var/lib/rabbitmq")
    _must_contain(compose, "postgres_data:")
    _must_contain(compose, "rabbitmq_data:")


def test_netaegis_compose_has_redis_service_and_dependency():
    compose = "netaegis/docker-compose.yml"
    _must_contain(compose, "redis:")
    _must_contain(compose, "image: redis:7-alpine")
    _must_contain(compose, "depends_on:")
    _must_contain(compose, "condition: service_healthy")


def test_ci_has_matrix_and_contract_jobs():
    workflow = ".github/workflows/ci.yml"
    _must_contain(workflow, "python-checks:")
    _must_contain(workflow, "repository-contracts:")
    _must_contain(workflow, "strategy:")
    _must_contain(workflow, "matrix:")
    _must_contain(workflow, "pytest -q tests/test_repository_contract.py")


def test_service_main_files_expose_advanced_routes():
    expectations = {
        "cloudbudget/api/main.py": ["/api/v1/costs", "/api/v1/costs/summary", "/api/v1/costs/top"],
        "infraflow/engine/main.py": ["/api/v1/servers", "/api/v1/servers/{server_name}", "/api/v1/runbooks/execute"],
        "netguardian/engine/main.py": ["/api/v1/alerts"],
        "netaegis/server/main_mcp/main.py": ["/api/v1/status", "/api/v1/components"],
    }
    for path, routes in expectations.items():
        content = _read(path)
        for route in routes:
            assert route in content, f"Missing route '{route}' in {path}"


def test_service_main_files_include_initialization_logic():
    checks = {
        "cloudbudget/api/main.py": ["init_db", "lifespan"],
        "infraflow/engine/main.py": ["_initialize_state", "lifespan"],
        "netguardian/engine/main.py": ["_initialize_state", "lifespan"],
        "netaegis/server/main_mcp/main.py": ["/health", "timestamp"],
    }
    for path, tokens in checks.items():
        content = _read(path)
        for token in tokens:
            assert token in content, f"Missing initialization token '{token}' in {path}"


def test_service_test_suites_exist():
    required = [
        "cloudbudget/tests/test_main_summary.py",
        "infraflow/tests/test_main_api_extended.py",
        "netguardian/tests/test_main_api_extended.py",
        "netaegis/tests/test_health.py",
    ]
    for path in required:
        _must_exist(path)


def test_ci_matrix_executes_service_tests_and_compileall():
    workflow = _read(".github/workflows/ci.yml")
    assert "python -m compileall" in workflow, "CI must run compileall checks"
    assert "pytest -q tests/test_main_summary.py" in workflow
    assert "pytest -q tests/test_main_api_extended.py" in workflow
    assert "pytest -q tests/test_health.py" in workflow


def test_service_entrypoints_have_app_versioning():
    files = [
        "cloudbudget/api/main.py",
        "infraflow/engine/main.py",
        "netguardian/engine/main.py",
        "netaegis/server/main_mcp/main.py",
    ]
    for path in files:
        content = _read(path)
        assert "version=" in content, f"Missing FastAPI version in {path}"


def test_ci_installs_service_requirements():
    workflow = _read(".github/workflows/ci.yml")
    assert "pip install -r ${{ matrix.requirements }}" in workflow
    assert "actions/setup-python@v5" in workflow


def test_pyproject_contains_project_metadata():
    pyprojects = [
        "cloudbudget/pyproject.toml",
        "infraflow/pyproject.toml",
        "netguardian/pyproject.toml",
    ]
    for path in pyprojects:
        content = _read(path)
        assert "[project]" in content, f"Missing [project] section in {path}"
        assert "name =" in content, f"Missing project name in {path}"
        assert "version =" in content, f"Missing project version in {path}"
        assert "requires-python" in content, f"Missing requires-python in {path}"


def test_ci_has_repository_contract_command_exactly_once():
    workflow = _read(".github/workflows/ci.yml")
    count = workflow.count("pytest -q tests/test_repository_contract.py")
    assert count == 1, f"Expected exactly one repository-contract command, found {count}"


def test_requirements_files_reference_runtime_dependencies():
    checks = {
        "cloudbudget/requirements.txt": "api/requirements.txt",
        "infraflow/requirements.txt": "engine/requirements.txt",
        "netguardian/requirements.txt": "engine/requirements.txt",
    }
    for path, expected in checks.items():
        content = _read(path)
        assert expected in content, f"Expected '{expected}' reference in {path}"


def test_cloudbudget_health_route_contains_service_and_timestamp_tokens():
    content = _read("cloudbudget/api/main.py")
    assert '"/health"' in content
    assert '"service": "cloudbudget-api"' in content
    assert '"timestamp"' in content


def test_netaegis_env_includes_redis_url():
    content = _read("netaegis/.env.example")
    assert "REDIS_URL=" in content, "Missing REDIS_URL in netaegis/.env.example"


def test_infraflow_env_has_notification_keys():
    content = _read("infraflow/.env.example")
    for key in ["SLACK_WEBHOOK=", "SMTP_HOST=", "SMTP_PORT=", "EMAIL_FROM=", "EMAIL_TO="]:
        assert key in content, f"Missing {key} in infraflow/.env.example"


def test_netguardian_env_has_optional_integration_keys():
    content = _read("netguardian/.env.example")
    for key in ["ABUSEIPDB_API_KEY=", "SLACK_WEBHOOK_URL=", "MISP_URL=", "MISP_KEY="]:
        assert key in content, f"Missing {key} in netguardian/.env.example"


def test_cloudbudget_env_has_celery_keys():
    content = _read("cloudbudget/.env.example")
    for key in ["CELERY_BROKER_URL=", "CELERY_RESULT_BACKEND="]:
        assert key in content, f"Missing {key} in cloudbudget/.env.example"
