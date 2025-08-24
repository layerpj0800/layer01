import re
import httpx

async def fetch_link_preview(url: str) -> dict[str, str]:
    """Fetch basic metadata for a URL for preview purposes."""
    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        resp = await client.get(url)
        text = resp.text

    def _search(pattern: str) -> str | None:
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else None

    title = _search(r"<title[^>]*>(.*?)</title>") or ""
    description = _search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']') or ""
    image = _search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']') or ""

    return {"title": title, "description": description, "image": image, "url": url}
