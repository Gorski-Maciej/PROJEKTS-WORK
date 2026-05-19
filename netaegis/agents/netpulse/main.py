from fastapi import FastAPI

app = FastAPI(title="NetAegis NetPulse Agent")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "netpulse"}
