import os
import asyncio

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_SECRET"] = "testsecret"
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

    r_list = client.get(f"/api/v1/subscriptions/plans/1")
    assert r_list.status_code == 200
    assert len(r_list.json()) == 1

    subscriber_headers = _auth_header("sub@example.com")
    r2 = client.post(
        "/api/v1/subscriptions/",
        json={"plan_id": plan_id},
        headers=subscriber_headers,
    )
    assert r2.status_code == 200
    assert r2.json()["status"] == "pending"
    merchant_uid = r2.json()["merchant_uid"]
    sub_id = r2.json()["id"]

    r_verify = client.post(
        "/api/v1/subscriptions/verify-payment",
        json={"merchant_uid": merchant_uid},
    )
    assert r_verify.status_code == 200
    assert r_verify.json()["status"] == "active"

    new_date = "2030-01-01T00:00:00"
    r_update = client.put(
        f"/api/v1/subscriptions/{sub_id}",
        json={"current_period_end": new_date},
        headers=subscriber_headers,
    )
    assert r_update.status_code == 200
    assert r_update.json()["current_period_end"].startswith("2030-01-01")

    r_me = client.get("/api/v1/subscriptions/me", headers=subscriber_headers)
    assert r_me.status_code == 200
    assert r_me.json()["status"] == "active"


def test_verify_payment_failure():
    r = client.post(
        "/api/v1/subscriptions/verify-payment",
        json={"merchant_uid": "missing"},
    )
    assert r.status_code == 404
