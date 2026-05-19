from __future__ import annotations

import time
from dataclasses import dataclass

import requests


@dataclass
class HealthSpec:
    endpoint: str = "/health"
    method: str = "GET"
    expected_status: tuple[int, ...] = (200, 301)
    timeout: int = 5
    interval: int = 20


def check_api(base_url: str, spec: HealthSpec) -> bool:
    resp = requests.request(spec.method, f"{base_url}{spec.endpoint}", timeout=spec.timeout)
    return resp.status_code in spec.expected_status


def with_backoff(func, retries: int = 5, base_delay: float = 0.5) -> bool:
    for attempt in range(retries):
        if func():
            return True
        time.sleep(base_delay * (2 ** attempt))
    return False


def check_readiness(checks: list[tuple[str, callable]]) -> dict[str, bool]:
    return {name: with_backoff(fn) for name, fn in checks}
