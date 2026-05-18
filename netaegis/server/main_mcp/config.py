from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = "NetAegis Main MCP"
    main_db_url: str = "sqlite+aiosqlite:///./main_mcp.db"
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

settings = Settings()
