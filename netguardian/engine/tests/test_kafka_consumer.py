from __future__ import annotations

from types import SimpleNamespace

import pytest

from consumer import kafka_consumer


class DummyRedis:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    async def xadd(self, key, value):
        self.calls.append(("xadd", key, value))

    async def expire(self, key, ttl):
        self.calls.append(("expire", key, ttl))


class _AcquireCtx:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        return False


class DummyPool:
    def __init__(self) -> None:
        self.conn = SimpleNamespace(execute=self._execute)
        self.executed: list[tuple] = []

    def acquire(self):
        return _AcquireCtx(self.conn)

    async def _execute(self, query, *args):
        self.executed.append((query, args))


class DummyDuck:
    def __init__(self) -> None:
        self.executed: list[tuple] = []

    def execute(self, query, params=None):
        self.executed.append((query, params))


class DummyDNS:
    def __init__(self) -> None:
        self.domains: list[str] = []

    async def analyze_query(self, domain: str):
        self.domains.append(domain)


class DummyExfil:
    def __init__(self) -> None:
        self.checked: list[dict] = []

    async def check_volume(self, flow: dict):
        self.checked.append(flow)


@pytest.mark.asyncio
async def test_store_flow_persists_and_triggers_dns(monkeypatch):
    async def fake_enrich(flow):
        return {**flow, "abuse_score": 10}

    monkeypatch.setattr(kafka_consumer, "enrich_flow", fake_enrich)

    redis_conn = DummyRedis()
    db_pool = DummyPool()
    duck_con = DummyDuck()
    dns_detector = DummyDNS()
    exfil_detector = DummyExfil()

    flow = {
        "timestamp": "1700000000",
        "agent_id": "agent-01",
        "src_ip": "10.0.0.2",
        "dst_ip": "8.8.8.8",
        "src_port": 53000,
        "dst_port": 53,
        "proto": 17,
        "flags": "",
        "length": 120,
        "domain": "example.com",
    }

    await kafka_consumer.store_flow(
        redis_conn,
        db_pool,
        duck_con,
        flow,
        dns_detector,
        exfil_detector,
    )

    assert any(c[0] == "xadd" for c in redis_conn.calls)
    assert any(c[0] == "expire" for c in redis_conn.calls)
    assert dns_detector.domains == ["example.com"]
    assert len(db_pool.executed) == 1
    assert len(duck_con.executed) == 2
    assert exfil_detector.checked
