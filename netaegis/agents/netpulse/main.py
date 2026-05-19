from fastapi import FastAPI

app = FastAPI(title="NetAegis NetPulse Agent")

@app.get("/health")
def health():
    return {"status": "ok", "service": "netpulse"}
