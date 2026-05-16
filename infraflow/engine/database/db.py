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
        await c.execute("SELECT create_hypertable('metrics', 'time', if_not_exists => TRUE);")

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
        await c.execute(
            '''
            CREATE TABLE IF NOT EXISTS server_state (
              server_name TEXT PRIMARY KEY,
              last_cpu DOUBLE PRECISION,
              last_memory DOUBLE PRECISION,
              last_disk DOUBLE PRECISION,
              status TEXT NOT NULL DEFAULT 'unknown'
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
        if metric_type == 'cpu':
            await c.execute(
                """
                INSERT INTO server_state (server_name, last_cpu, status)
                VALUES ($1,$2,'online')
                ON CONFLICT (server_name)
                DO UPDATE SET last_cpu = EXCLUDED.last_cpu, status = 'online'
                """,
                server,
                value,
            )
        elif metric_type == 'memory':
            await c.execute(
                """
                INSERT INTO server_state (server_name, last_memory, status)
                VALUES ($1,$2,'online')
                ON CONFLICT (server_name)
                DO UPDATE SET last_memory = EXCLUDED.last_memory, status = 'online'
                """,
                server,
                value,
            )
        elif metric_type == 'disk':
            await c.execute(
                """
                INSERT INTO server_state (server_name, last_disk, status)
                VALUES ($1,$2,'online')
                ON CONFLICT (server_name)
                DO UPDATE SET last_disk = EXCLUDED.last_disk, status = 'online'
                """,
                server,
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


async def get_server_status(pool: Any, server_name: str) -> dict[str, Any]:
    async with pool.acquire() as c:
        row = await c.fetchrow(
            '''
            SELECT
              s.server_name,
              s.last_cpu,
              s.last_memory,
              s.last_disk,
              s.status,
              COALESCE(i.alerts, 0) AS alerts
            FROM server_state s
            LEFT JOIN (
                SELECT server_name, COUNT(*) AS alerts
                FROM incidents
                GROUP BY server_name
            ) i ON i.server_name = s.server_name
            WHERE s.server_name = $1
            ''',
            server_name,
        )
    return dict(row) if row else {}


async def get_latest_incidents(pool: Any, limit: int = 50) -> list[dict[str, Any]]:
    async with pool.acquire() as c:
        rows = await c.fetch(
            'SELECT time, server_name, description, priority FROM incidents ORDER BY time DESC LIMIT $1',
            limit,
        )
    return [dict(r) for r in rows]


async def detect_anomalies(pool: Any, server_name: str, min_points: int = 30) -> bool:
    from core.anomaly_predictor import AnomalyPredictor

    if not hasattr(pool, 'acquire'):
        return False
    async with pool.acquire() as c:
        rows = await c.fetch(
            "SELECT value FROM metrics WHERE server_name = $1 AND metric_type = 'cpu' ORDER BY time DESC LIMIT 200",
            server_name,
        )
    history = [float(r['value']) for r in reversed(rows)]
    if len(history) < min_points:
        return False
    predictor = AnomalyPredictor()
    predictor.fit(history[:-5])
    return predictor.predict(history[-5:])
