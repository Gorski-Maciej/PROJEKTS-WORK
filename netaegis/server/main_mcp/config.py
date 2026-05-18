from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "NetAegis Main MCP"
    main_db_url: str = "sqlite+aiosqlite:///./main_mcp.db"
    redis_url: str = "redis://localhost:6379/0"

settings = Settings()

REDIS_URL = "redis://redis:6379/0"
