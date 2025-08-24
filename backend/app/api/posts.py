"""Post API endpoints.

Provides access to posts within a channel.
"""

from fastapi import APIRouter, Request

from app.core.constants import DEFAULT_CHANNEL_ID, DEFAULT_POST_ID
from app.core.logger import write_log

router = APIRouter(prefix="/channels/{channel_id}/posts", tags=["posts"])

POSTS = {
    DEFAULT_CHANNEL_ID: [
        {
            "id": DEFAULT_POST_ID,
            "channel_id": DEFAULT_CHANNEL_ID,
            "title": "welcome",
            "content": "hello",
        }
    ]
}


@router.get("/")
async def list_posts(channel_id: int, request: Request) -> list[dict[str, int | str]]:
    """Return posts for a channel.

    Args:
        channel_id: Identifier of the channel.
        request: Incoming HTTP request.

    Returns:
        List of posts in the channel.
    """
    response_data = POSTS.get(channel_id, [])
    log_text = f"REQUEST {request.method} {request.url}\nRESPONSE {response_data}"
    write_log("posts", log_text)
    return response_data
