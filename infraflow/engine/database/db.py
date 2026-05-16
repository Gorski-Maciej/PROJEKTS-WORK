from __future__ import annotations

from typing import Any


async def init_db(pool: Any) -> None:
    async with pool.acquire() as c:
        await c.execute(
            '''
            CREATE TABLE IF NOT EXISTS metrics (
              time TIMESTAMPTZ DEFAULT NOW(),
              server_name TEXT NOT NULL,
              metric_type TEXT NOT NULL,
              value DOUBLE PRECISION NOT NULL
            );
            '''
        )
        await c.execute(
            '''
            CREATE TABLE IF NOT EXISTS incidents (
              id SERIAL PRIMARY KEY,
              time TIMESTAMPTZ DEFAULT NOW(),
              server_name TEXT NOT NULL,
              description TEXT NOT NULL,
              priority TEXT NOT NULL DEFAULT 'info'
            );
            '''
        )


async def save_metric(pool: Any, server: str, metric_type: str, value: float) -> None:
    async with pool.acquire() as c:
        await c.execute(
            'INSERT INTO metrics (server_name, metric_type, value) VALUES ($1,$2,$3)',
            server,
            metric_type,
            value,
        )


async def log_incident(pool: Any, server: str, description: str, priority: str = 'info') -> None:
    async with pool.acquire() as c:
        await c.execute(
            'INSERT INTO incidents (server_name, description, priority) VALUES ($1,$2,$3)',
            server,
            description,
            priority,
        )


async def get_latest_incidents(pool: Any, limit: int = 50) -> list[dict[str, Any]]:
    async with pool.acquire() as c:
        rows = await c.fetch(
            'SELECT time, server_name, description, priority FROM incidents ORDER BY time DESC LIMIT $1',
            limit,
        )
    return [dict(r) for r in rows]
