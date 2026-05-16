from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator

AGENTS_ONLINE = Gauge('netguardian_agents_online', 'Number of agents with live heartbeat')


def setup_metrics(app):
    Instrumentator().instrument(app).expose(app)


async def update_agent_gauge(redis_client):
    count = 0
    async for _ in redis_client.scan_iter(match='agent:heartbeat:*'):
        count += 1
    AGENTS_ONLINE.set(count)
