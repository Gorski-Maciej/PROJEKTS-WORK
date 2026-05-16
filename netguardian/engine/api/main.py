import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager

import asyncpg
import duckdb
import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm

from api.auth import USERS, create_access_token, require_role
from consumer.kafka_consumer import start_kafka_consumer
from detection.beacon_detector import BeaconDetector
from detection.window_analyzer import analyze_window
from report.generator import generate_report
from threat_intel.misp_sync import sync_blacklist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:netguardian@timescaledb:5432/netguardian")
DUCKDB_PATH = os.getenv("DUCKDB_PATH", "/data/netguardian.db")

redis_client = None
db_pool = None
duck_con = None
beacon_detector = None


async def init_timescale(pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS flows (
                time TIMESTAMPTZ NOT NULL,
                agent_id TEXT,
                src_ip INET,
                dst_ip INET,
                src_port INTEGER,
                dst_port INTEGER,
                proto INTEGER,
                flags TEXT,
                length INTEGER
            );
            """
        )
        await conn.execute("SELECT create_hypertable('flows', 'time', if_not_exists => TRUE);")


async def periodic_beacon_analysis():
    while True:
        await asyncio.sleep(300)
        if beacon_detector:
            await beacon_detector.analyze_beacons()




async def periodic_misp_sync():
    while True:
        await asyncio.sleep(900)
        if redis_client:
            await sync_blacklist(redis_client)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client, db_pool, duck_con, beacon_detector
    redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    await init_timescale(db_pool)
    duck_con = duckdb.connect(DUCKDB_PATH)
    beacon_detector = BeaconDetector(redis_client)

    asyncio.create_task(start_kafka_consumer(redis_client, db_pool, duck_con, beacon_detector))
    asyncio.create_task(periodic_analysis())
    asyncio.create_task(periodic_beacon_analysis())
    asyncio.create_task(periodic_misp_sync())
    yield

    await db_pool.close()
    duck_con.close()
    await redis_client.close()


app = FastAPI(lifespan=lifespan)


@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form_data.username)
    if not user or user['password'] != form_data.password:
        raise HTTPException(401, detail='Bad credentials')
    token = create_access_token({'sub': form_data.username})
    return {'access_token': token, 'token_type': 'bearer'}


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('alerts')
    try:
        while True:
            msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if msg and msg.get('type') == 'message':
                await websocket.send_text(msg['data'])
            await asyncio.sleep(0.1)
    finally:
        await pubsub.unsubscribe('alerts')
        await pubsub.close()


@app.get('/status')
async def status(user=Depends(require_role('readonly'))):
    return {
        'alerts_count': await redis_client.llen('alerts_list'),
        'blocked_ips': list(await redis_client.smembers('blocked_ips')),
    }


@app.post('/unblock/{ip}')
async def unblock_ip(ip: str, user=Depends(require_role('admin'))):
    await redis_client.srem('blocked_ips', ip)
    return {'status': 'unblocked', 'ip': ip}


@app.get('/report')
async def get_report(user=Depends(require_role('readonly'))):
    report_path = await generate_report(db_pool, duck_con, redis_client)
    return FileResponse(report_path, media_type='application/pdf', filename='netguardian_report.pdf')


@app.post('/alert/{alert_id}/tag')
async def tag_alert(alert_id: str, tag: str, user=Depends(require_role('admin'))):
    await redis_client.hset(f'alert_tag:{alert_id}', 'tag', tag)
    return {'status': 'tagged', 'alert_id': alert_id, 'tag': tag}


async def periodic_analysis():
    while True:
        await asyncio.sleep(10)
        await analyze_window(redis_client)
