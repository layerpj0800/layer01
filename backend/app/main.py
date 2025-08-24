from fastapi import FastAPI

from .core.config import settings


from .api import auth, payments, subscriptions, messages



app = FastAPI(title="Layer01 API")


app.include_router(auth.router)
app.include_router(subscriptions.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:

    return {"message": "Hello, world"}
