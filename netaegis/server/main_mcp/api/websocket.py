from fastapi import APIRouter, WebSocket

router = APIRouter(tags=["websocket"])


@router.websocket('/ws/live')
async def live_ws(ws: WebSocket):
    await ws.accept()
    await ws.send_json({'type': 'welcome', 'message': 'live stream initialized'})
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_json({'type': 'echo', 'message': data})
    except Exception:
        await ws.close()
