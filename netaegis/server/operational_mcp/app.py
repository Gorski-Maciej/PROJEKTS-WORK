from fastapi import FastAPI
from server.operational_mcp.api.agents import router as agents_router
from server.operational_mcp.api.sync import router as sync_router
from server.operational_mcp.api.actions import router as actions_router
from server.operational_mcp.api.status import router as status_router
from server.operational_mcp.core.state import OperationalState

app = FastAPI(title="NetAegis Operational MCP", version="0.5.0")
app.state.state = OperationalState()
app.state.main_mcp_url = "http://localhost:8000"
app.state.node_id = "op-mcp-1"

app.include_router(agents_router)
app.include_router(sync_router)
app.include_router(actions_router)
app.include_router(status_router)
