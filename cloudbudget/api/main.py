from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CloudBudget API")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/costs")
def get_costs():
    return [
        {"id": 1, "service": "EC2", "amount": 150.0, "date": "2024-01-01"},
        {"id": 2, "service": "RDS", "amount": 200.0, "date": "2024-01-01"},
        {"id": 3, "service": "S3", "amount": 50.0, "date": "2024-01-01"}
    ]
