from __future__ import annotations

import asyncio
import json
import os
import signal

import asyncpg
import redis.asyncio as redis

from core.config_loader import load_config
from core.context import RepairContext
from worker.executor import execute_checks_for_server


async def process_job(job: dict, ctx: RepairContext) -> None:
    server = job.get('server')
    if not server:
        return
    await execute_checks_for_server(server, ctx)


async def process_queue() -> None:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:infraflow@localhost:5432/infraflow')

    r = redis.Redis(host=redis_host, decode_responses=True)
    db_pool = await asyncpg.create_pool(db_url)
    cfg = {s['name']: s for s in load_config().get('servers', [])}

    stop_event = asyncio.Event()

    def _handle_stop(*_: object) -> None:
        stop_event.set()

    signal.signal(signal.SIGTERM, _handle_stop)
    signal.signal(signal.SIGINT, _handle_stop)

    while not stop_event.is_set():
        item = await r.blpop('infraflow:jobs', timeout=5)
        if not item:
            await asyncio.sleep(0.1)
            continue
        _, payload = item
        data = json.loads(payload)
        server = cfg.get(data.get('server'))
        if not server:
            continue
        try:
            await process_job({'server': server}, RepairContext(db_pool=db_pool, redis=r))
        except Exception as exc:
            await r.rpush('infraflow:dlq', json.dumps({'server': server.get('name'), 'payload': data, 'error': str(exc)}))

    await db_pool.close()
    await r.close()


if __name__ == '__main__':
    asyncio.run(process_queue())
