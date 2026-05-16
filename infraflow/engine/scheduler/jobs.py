from __future__ import annotations

import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from core.config_loader import load_config
from core.anomaly_predictor import predictor

scheduler = AsyncIOScheduler()


async def periodic_training(db_pool):
    config = load_config()
    for server in config.get('servers', []):
        try:
            await predictor.train(db_pool, server['name'], hours=168)
        except Exception:
            pass


def setup_scheduler(redis_client, db_pool):
    config = load_config()
    for s in config.get('servers', []):
        interval = s.get('check_interval', config.get('global', {}).get('check_interval', 300))

        async def enqueue_job(server_name: str = s['name']):
            await redis_client.rpush('infraflow:jobs', json.dumps({'server': server_name}))

        scheduler.add_job(
            enqueue_job,
            IntervalTrigger(seconds=interval),
            id=f"check_{s['name']}",
            replace_existing=True,
        )
    scheduler.add_job(
        periodic_training,
        IntervalTrigger(hours=6),
        args=[db_pool],
        id='ml_training',
        replace_existing=True,
    )
    scheduler.start()
