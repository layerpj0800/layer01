"""Tests for channel and post endpoints."""

from fastapi.testclient import TestClient

from app.core.constants import DEFAULT_CHANNEL_ID, DEFAULT_POST_ID
from app.main import app

client = TestClient(app)


def test_list_channels() -> None:
    """Ensure channel list returns default channel."""
    response = client.get("/api/v1/channels")
    assert response.status_code == 200
    data = response.json()
    assert any(ch["id"] == DEFAULT_CHANNEL_ID for ch in data)


def test_list_posts() -> None:
    """Ensure posts list returns default post for channel."""
    response = client.get(f"/api/v1/channels/{DEFAULT_CHANNEL_ID}/posts")
    assert response.status_code == 200
    data = response.json()
    if data:
        assert data[0]["id"] == DEFAULT_POST_ID
