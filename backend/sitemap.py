import httpx
from urllib.parse import urljoin, urlparse
import asyncio

async def _fetch_text(url: str, client: httpx.AsyncClient) -> str:
    try:
        resp = await client.get(url, timeout=10.0, follow_redirects=True)
        if resp.status_code == 200:
            return resp.text
    except httpx.RequestError:
        pass
    return ""

async def fetch_sitemap_links(base: str, client: httpx.AsyncClient) -> list:
    """Fetch ``/sitemap.xml`` and extract <loc> URLs.
    Returns a list of absolute URLs.
    """
    parsed = urlparse(base)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    text = await _fetch_text(sitemap_url, client)
    if not text:
        return []
    import re
    locs = re.findall(r'<loc>([^<]+)</loc>', text, flags=re.IGNORECASE)
    return [urljoin(base, loc.strip()) for loc in locs]

async def fetch_robots_links(base: str, client: httpx.AsyncClient) -> list:
    """Fetch ``/robots.txt`` and extract Disallow/Allow paths as URLs.
    Returns a list of absolute URLs.
    """
    parsed = urlparse(base)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    text = await _fetch_text(robots_url, client)
    if not text:
        return []
    links = []
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith('disallow:') or line.lower().startswith('allow:'):
            path = line.split(':', 1)[1].strip()
            if path:
                links.append(urljoin(base, path))
    return links
