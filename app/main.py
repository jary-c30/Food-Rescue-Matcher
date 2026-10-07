from fastapi import FastAPI

app = FastAPI(title="Food Rescue Matcher")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
