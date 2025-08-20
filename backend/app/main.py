from fastapi import FastAPI

from .core.config import settings
from .api import auth

app = FastAPI(title="Layer01 API")


app.include_router(auth.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, world"}
