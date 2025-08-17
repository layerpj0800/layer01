from fastapi import FastAPI

from .core.config import settings

app = FastAPI(title="Layer01 API")


@app.get("/")
async def root() -> dict[str, str]:
  return {"message": "Hello, world"}
