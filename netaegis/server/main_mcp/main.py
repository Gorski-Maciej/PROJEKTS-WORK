from fastapi import FastAPI

app = FastAPI(title="NetAegis Main MCP")


@app.get("/health")
def health() -> dict[str, str]:
    return {"service": "main_mcp"}
