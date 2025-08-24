"""Channel API endpoints.

Provides access to channel listings.
"""

from fastapi import APIRouter, Request

from app.core.logger import write_log
from app.core.constants import DEFAULT_CHANNEL_ID

router = APIRouter(prefix="/channels", tags=["channels"])

CHANNELS = [
    {"id": DEFAULT_CHANNEL_ID, "name": "alpha", "description": "demo"}
]


@router.get("/")
async def list_channels(request: Request) -> list[dict[str, int | str]]:
    """Return available channels.

    Args:
        request: Incoming HTTP request.

    Returns:
        List of channels.
    """
    response_data = CHANNELS
    log_text = f"REQUEST {request.method} {request.url}\nRESPONSE {response_data}"
    write_log("channels", log_text)
    return response_data
