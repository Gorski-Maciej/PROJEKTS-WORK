import asyncio

from consumer.heartbeat_consumer import store_heartbeat


class DummyRedis:
    def __init__(self):
        self.calls = []

    async def set(self, key, value, ex=None):
        self.calls.append((key, value, ex))


def test_store_heartbeat_sets_ttl_key():
    r = DummyRedis()
    asyncio.run(store_heartbeat(r, {"agent_id": "agent-01", "timestamp": 123.45}))
    assert r.calls[0][0] == "agent:heartbeat:agent-01"
    assert r.calls[0][2] == 30
