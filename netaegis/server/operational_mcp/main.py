from fastapi import FastAPI

app = FastAPI(title="NetAegis Operational MCP")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "operational-mcp"}
