from fastapi import FastAPI

app = FastAPI(title="NetAegis NetConfig Agent")

@app.get("/health")
def health():
    return {"status": "ok", "service": "netconfig"}
