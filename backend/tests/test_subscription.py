import os
import asyncio

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_SECRET"] = "testsecret"
os.environ["CORS_ORIGINS"] = "*"
os.environ["S3_BUCKET"] = "test"
os.environ["IAMPORT_API_KEY"] = "test"
os.environ["IAMPORT_API_SECRET"] = "test"
os.environ["IAMPORT_WEBHOOK_SECRET"] = "whsec"

from fastapi.testclient import TestClient  # noqa: E402

from app.core.database import Base, engine, async_session  # noqa: E402
from app.main import app  # noqa: E402
from app.auth.security import get_password_hash  # noqa: E402
from app.models import Channel, User  # noqa: E402


async def _seed_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        creator = User(
            email="creator@example.com",
            password_hash=get_password_hash("secret"),
            role="creator",
        )
        subscriber = User(
            email="sub@example.com",
            password_hash=get_password_hash("secret"),
        )
        session.add_all([creator, subscriber])
        await session.flush()
        channel = Channel(creator_id=creator.id, title="Test Channel")
        session.add(channel)
        await session.commit()


asyncio.get_event_loop().run_until_complete(_seed_db())
client = TestClient(app)


def _auth_header(email: str) -> dict[str, str]:
    r = client.post("/api/v1/auth/login", json={"email": email, "password": "secret"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_plan_and_subscription_flow():
    creator_headers = _auth_header("creator@example.com")
    r = client.post(
        "/api/v1/subscriptions/plans",
        json={"channel_id": 1, "price": 1000},
        headers=creator_headers,
    )
    assert r.status_code == 200
    plan_id = r.json()["id"]

    subscriber_headers = _auth_header("sub@example.com")
    r2 = client.post(
        "/api/v1/subscriptions/",
        json={"plan_id": plan_id},
        headers=subscriber_headers,
    )
    assert r2.status_code == 200
    merchant_uid = r2.json()["merchant_uid"]

    r3 = client.post(
        "/api/v1/payments/iamport-webhook",
        json={"merchant_uid": merchant_uid, "status": "paid"},
        headers={"X-Iamport-Signature": "whsec"},
    )
    assert r3.status_code == 200
