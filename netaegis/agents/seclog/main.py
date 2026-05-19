from fastapi import FastAPI

app = FastAPI(title="NetAegis SecLog Agent")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "seclog"}
