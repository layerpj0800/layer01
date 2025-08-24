from fastapi import APIRouter, HTTPException, Query

from app.services.link_preview import fetch_link_preview

router = APIRouter(prefix="/link-preview", tags=["link-preview"])


@router.get("/")
async def generate_link_preview(url: str = Query(..., description="URL to preview")):
    try:
        return await fetch_link_preview(url)
    except Exception as exc:  # pragma: no cover - simple pass-through
        raise HTTPException(status_code=400, detail=str(exc))
