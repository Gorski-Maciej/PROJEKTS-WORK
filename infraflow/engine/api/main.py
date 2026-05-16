from __future__ import annotations

import asyncio
import os

import asyncpg
import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from fastapi.responses import Response
from prometheus_fastapi_instrumentator import Instrumentator

from api.auth import USERS, create_access_token, verify_token
from core.config_loader import load_config
from database.db import get_latest_incidents, init_db
from scheduler.jobs import setup_scheduler

app = FastAPI(title='InfraFlow API')
state: dict[str, object] = {'redis': None, 'db': None}


@app.on_event('startup')
async def startup() -> None:
    state['redis'] = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), decode_responses=True)
    state['db'] = await asyncpg.create_pool(os.getenv('DATABASE_URL', 'postgresql://postgres:infraflow@localhost:5432/infraflow'))
    await init_db(state['db'])
    setup_scheduler(state['redis'], state['db'])
    Instrumentator().instrument(app).expose(app)


@app.post('/token')
async def token(username: str, password: str) -> dict[str, str]:
    u = USERS.get(username)
    if not u or u['password'] != password:
        return {'error': 'invalid credentials'}
    return {'access_token': create_access_token({'sub': username, 'role': u['role']}), 'token_type': 'bearer'}


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.get('/servers')
async def servers(_: dict = Depends(verify_token)) -> list[dict]:
    return load_config().get('servers', [])


@app.post('/servers/{server_name}/run-checks')
async def run_checks(server_name: str, _: dict = Depends(verify_token)) -> dict[str, str]:
    cfg = load_config().get('servers', [])
    server = next((s for s in cfg if s['name'] == server_name), None)
    if not server:
        raise HTTPException(status_code=404, detail='server not found')
    await state['redis'].rpush('infraflow:jobs', f'{{"server":"{server_name}"}}')
    return {'status': 'queued'}


@app.get('/incidents')
async def incidents(limit: int = 50, _: dict = Depends(verify_token)) -> list[dict]:
    return await get_latest_incidents(state['db'], limit)


@app.get('/queue-depth')
async def queue_depth(_: dict = Depends(verify_token)) -> dict[str, int]:
    depth = await state['redis'].llen('infraflow:jobs')
    return {'jobs': int(depth)}


@app.websocket('/ws')
async def ws(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_json({'status': 'connected'})
    while True:
        await asyncio.sleep(5)
        await websocket.send_json({'status': 'alive'})


@app.get('/metrics')
async def metrics() -> Response:
    from prometheus_client import generate_latest

    return Response(generate_latest(), media_type='text/plain')
