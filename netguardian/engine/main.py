from fastapi import FastAPI

app = FastAPI(title="NetGuardian API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/alerts")
def get_alerts():
    return [
        {"id": 1, "message": "DDoS attack detected", "severity": "high"},
        {"id": 2, "message": "Port scan from 10.0.0.5", "severity": "medium"}
    ]
