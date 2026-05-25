from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="CloudBudget Agents", version="1.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "cloudbudget-agents", "timestamp": datetime.now(timezone.utc).isoformat()}
