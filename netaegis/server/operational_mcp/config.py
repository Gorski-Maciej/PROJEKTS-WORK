from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "NetAegis Operational MCP"
    main_mcp_url: str = "http://localhost:8000"
    local_db_url: str = "sqlite+aiosqlite:///./operational_mcp.db"

settings = Settings()
