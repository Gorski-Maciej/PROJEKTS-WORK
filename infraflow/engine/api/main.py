from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path

import asyncpg
import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from prometheus_fastapi_instrumentator import Instrumentator

from api.auth import USERS, create_access_token, verify_token
from core.config_loader import CONFIG_PATH, load_config
from core.config_versioning import commit_config_change
from database.db import get_latest_incidents, get_server_status, init_db
from worker.executor import execute_action
from core.context import RepairContext
from scheduler.jobs import setup_scheduler

app = FastAPI(title='InfraFlow API')
state: dict[str, object] = {'redis': None, 'db': None}
TOKEN_ATTEMPTS: dict[str, list[float]] = {}


@app.on_event('startup')
async def startup() -> None:
    state['redis'] = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), decode_responses=True)
    state['db'] = await asyncpg.create_pool(os.getenv('DATABASE_URL', 'postgresql://postgres:infraflow@localhost:5432/infraflow'))
    await init_db(state['db'])
    setup_scheduler(state['redis'], state['db'])
    Instrumentator().instrument(app).expose(app)


@app.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    now = time.time()
    attempts = [t for t in TOKEN_ATTEMPTS.get(form_data.username, []) if now - t < 60]
    if len(attempts) >= 5:
        raise HTTPException(status_code=429, detail='too many login attempts')

    u = USERS.get(form_data.username)
    if not u or u['password'] != form_data.password:
        attempts.append(now)
        TOKEN_ATTEMPTS[form_data.username] = attempts
        raise HTTPException(status_code=401, detail='invalid credentials')
    TOKEN_ATTEMPTS[form_data.username] = []
    return {'access_token': create_access_token({'sub': form_data.username, 'role': u['role']}), 'token_type': 'bearer'}


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.get('/servers')
async def servers(_: dict = Depends(verify_token)) -> list[dict]:
    return load_config().get('servers', [])


@app.get('/servers/{server_name}/status')
async def server_status(server_name: str, _: dict = Depends(verify_token)) -> dict:
    status = await get_server_status(state['db'], server_name)
    if not status:
        raise HTTPException(status_code=404, detail='server status not found')
    return status


@app.post('/servers/{server_name}/run-checks')
async def run_checks(server_name: str, _: dict = Depends(verify_token)) -> dict[str, str]:
    cfg = load_config().get('servers', [])
    server = next((s for s in cfg if s['name'] == server_name), None)
    if not server:
        raise HTTPException(status_code=404, detail='server not found')
    await state['redis'].rpush('infraflow:jobs', f'{{"server":"{server_name}"}}')
    return {'status': 'queued'}




ALLOWED_MANUAL_ACTIONS = {'restart_service', 'auto_patch', 'clean_logs'}


@app.post('/servers/{server_name}/actions/{action_type}')
async def run_manual_action(server_name: str, action_type: str, _: dict = Depends(verify_token)) -> dict[str, str]:
    cfg = load_config().get('servers', [])
    server = next((s for s in cfg if s['name'] == server_name), None)
    if not server:
        raise HTTPException(status_code=404, detail='server not found')
    if action_type not in ALLOWED_MANUAL_ACTIONS:
        raise HTTPException(status_code=400, detail='unsupported action type')

    action = {'type': action_type}
    if action_type == 'restart_service':
        action['target'] = 'nginx'
    elif action_type == 'clean_logs':
        action['path'] = '/var/log'
    await execute_action(server, action, RepairContext(db_pool=state['db'], redis=state['redis']))
    return {'status': 'executed'}




@app.put('/config/servers')
async def update_servers_config(payload: dict, claims: dict = Depends(verify_token)) -> dict[str, object]:
    if claims.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='admin role required')

    servers = payload.get('servers')
    if not isinstance(servers, list):
        raise HTTPException(status_code=400, detail='payload must contain servers list')

    cfg_path = Path(CONFIG_PATH)
    cfg_path.parent.mkdir(parents=True, exist_ok=True)

    import yaml

    with cfg_path.open('w', encoding='utf-8') as f:
        yaml.safe_dump(payload, f, sort_keys=False, allow_unicode=True)

    repo_root = str(cfg_path.parents[2]) if len(cfg_path.parents) >= 3 else str(cfg_path.parent)
    committed = commit_config_change(repo_root, 'engine/config/servers.yml', 'infraflow: update servers config')
    return {'status': 'updated', 'committed': committed}


@app.get('/incidents')
async def incidents(limit: int = 50, _: dict = Depends(verify_token)) -> list[dict]:
    return await get_latest_incidents(state['db'], limit)


@app.get('/queue-depth')
async def queue_depth(_: dict = Depends(verify_token)) -> dict[str, int]:
    depth = await state['redis'].llen('infraflow:jobs')
    return {'jobs': int(depth)}


@app.websocket('/ws')
async def ws(websocket: WebSocket) -> None:
    # Keep WS public for dashboard live feed while token-protected REST handles operations.
    await websocket.accept()
    await websocket.send_json({'status': 'connected'})

    pubsub = state['redis'].pubsub()
    await pubsub.subscribe('server_updates')
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5.0)
            if message and message.get('data'):
                await websocket.send_text(message['data'])
            else:
                await websocket.send_json({'status': 'alive'})
            await asyncio.sleep(0.2)
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe('server_updates')
        await pubsub.close()


@app.get('/metrics')
async def metrics() -> Response:
    from prometheus_client import generate_latest

    return Response(generate_latest(), media_type='text/plain')
