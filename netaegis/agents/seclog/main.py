from fastapi import FastAPI

app = FastAPI(title="NetAegis SecLog Agent")

@app.get("/health")
def health():
    return {"status": "ok", "service": "seclog"}
