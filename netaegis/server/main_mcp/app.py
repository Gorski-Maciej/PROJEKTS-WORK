from fastapi import FastAPI
from server.main_mcp.api.dashboard import router as dashboard_router
from server.main_mcp.api.incidents import router as incidents_router
from server.main_mcp.api.sync import router as sync_router
from server.main_mcp.api.actions import router as actions_router
from server.main_mcp.api.realtime import router as realtime_router
from server.main_mcp.api.policies import router as policies_router
from server.main_mcp.api.recommendations import router as recommendations_router
from server.main_mcp.api.chargeback import router as chargeback_router
from server.main_mcp.api.predictions import router as predictions_router
from server.main_mcp.api.websocket import router as websocket_router
from server.main_mcp.api.auth import router as auth_router
from server.main_mcp.core.store import MainStore
from server.main_mcp.services.event_processor import EventProcessor

app = FastAPI(title="NetAegis Main MCP", version="0.6.0")
app.state.store = MainStore()
app.state.processor = EventProcessor()
app.state.action_queue = []
app.state.policies = []

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(incidents_router)
app.include_router(sync_router)
app.include_router(actions_router)
app.include_router(realtime_router)
app.include_router(policies_router)
app.include_router(recommendations_router)
app.include_router(chargeback_router)
app.include_router(predictions_router)
app.include_router(websocket_router)
