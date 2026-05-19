import os
import pytest


@pytest.fixture
def service_url(request):
    service = request.param
    env_key = f"{service.upper()}_URL"
    return os.getenv(env_key, f"http://localhost:{request.getfixturevalue('service_port')}")


@pytest.fixture
def service_port(request):
    return request.param
