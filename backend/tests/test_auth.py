import os
import asyncio

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_SECRET"] = "testsecret"


os.environ["S3_BUCKET"] = "test"
os.environ["IAMPORT_API_KEY"] = "test"
os.environ["IAMPORT_API_SECRET"] = "test"
os.environ["IAMPORT_WEBHOOK_SECRET"] = "whsec"

from fastapi.testclient import TestClient  # noqa: E402

from app.core.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


async def _init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.get_event_loop().run_until_complete(_init_db())
client = TestClient(app)


def test_register_and_login():
    r = client.post(
        "/api/v1/auth/register", json={"email": "user@example.com", "password": "secret"}
    )
    assert r.status_code == 200
    r2 = client.post(
        "/api/v1/auth/login", json={"email": "user@example.com", "password": "secret"}
    )
    assert r2.status_code == 200
    token = r2.json()["access_token"]
    r3 = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert r3.status_code == 200
    assert r3.json()["email"] == "user@example.com"
