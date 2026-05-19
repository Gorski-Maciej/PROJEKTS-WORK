import yaml
from fastapi import FastAPI

app = FastAPI(title="InfraFlow API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/servers")
def list_servers():
    with open("/app/config/servers.yml") as f:
        config = yaml.safe_load(f)
    return config.get("servers", [])
