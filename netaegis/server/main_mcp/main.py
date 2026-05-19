from fastapi import FastAPI

app = FastAPI(title="NetAegis Main MCP")

@app.get("/health")
def health():
    return {"status": "ok", "service": "main_mcp"}
