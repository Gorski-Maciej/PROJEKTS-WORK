import importlib
import logging

from fastapi import APIRouter, FastAPI

from server.main_mcp.core.store import MainStore
from server.main_mcp.services.event_processor import EventProcessor

logger = logging.getLogger(__name__)

app = FastAPI(title="NetAegis Main MCP", version="0.6.0")
app.state.store = MainStore()
app.state.processor = EventProcessor()
app.state.action_queue = []
app.state.policies = []

ROUTER_MODULES = [
    "auth",
    "dashboard",
    "incidents",
    "sync",
    "actions",
    "realtime",
    "policies",
    "recommendations",
    "chargeback",
    "predictions",
    "websocket",
]


def load_router(module_name: str) -> APIRouter:
    try:
        module = importlib.import_module(f"server.main_mcp.api.{module_name}")
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            return router
        logger.error("Module '%s' does not expose APIRouter 'router'; using stub", module_name)
    except Exception as exc:
        logger.exception("Failed to import router module '%s': %s", module_name, exc)
    return APIRouter()


def safe_include_router(router: APIRouter, name: str) -> None:
    try:
        app.include_router(router)
    except Exception as exc:
        logger.exception("Failed to include router '%s': %s", name, exc)


for router_name in ROUTER_MODULES:
    safe_include_router(load_router(router_name), router_name)
