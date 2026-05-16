from fastapi import APIRouter, WebSocket
from datetime import datetime, timezone

router = APIRouter(tags=["realtime"])

@router.websocket('/ws/costs')
async def costs_ws(websocket: WebSocket):
    await websocket.accept()
    for _ in range(3):
        await websocket.send_json({"event": "heartbeat", "ts": datetime.now(timezone.utc).isoformat()})
    await websocket.close()
