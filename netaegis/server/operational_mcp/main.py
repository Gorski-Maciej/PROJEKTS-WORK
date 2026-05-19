from fastapi import FastAPI

app = FastAPI(title="NetAegis Operational MCP")

@app.get("/health")
def health():
    return {"status": "ok", "service": "operational_mcp"}
