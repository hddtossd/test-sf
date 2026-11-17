import asyncio
import uuid
from dataclasses import dataclass
from typing import List, Optional

import httpx
from .crawler import extract_links
from .sitemap import fetch_sitemap_links, fetch_robots_links
from .analyzer import analyze_response, ResourceInfo
from .database import record_scan_start, record_scan_result, update_scan_progress

@dataclass
class ScanConfig:
    target: str
    max_depth: int = 3
    max_urls: int = 1000
    request_delay: float = 0.5
    timeout: float = 10.0
    wordlist_path: Optional[str] = None

async def _fetch(url: str, client: httpx.AsyncClient, config: ScanConfig) -> Optional[ResourceInfo]:
    try:
        resp = await client.get(url, timeout=config.timeout, follow_redirects=True)
        info = analyze_response(url, resp)
        return info
    except httpx.RequestError:
        return None

async def _crawl(start_url: str, config: ScanConfig, client: httpx.AsyncClient, seen: set, depth: int, progress_callback):
    if depth > config.max_depth or len(seen) >= config.max_urls:
        return
    info = await _fetch(start_url, client, config)
    if info:
        await progress_callback(info)
    seen.add(start_url)
    # Extract internal links
    links = []
    if info and info.content_type.startswith("text/html") and info.body:
        links = extract_links(info.body, config.target)
    for link in links:
        if link not in seen:
            await asyncio.sleep(config.request_delay)
            await _crawl(link, config, client, seen, depth + 1, progress_callback)

async def start_scan(config: ScanConfig, background_tasks) -> str:
    """Kick off a background scan and return a scan_id."""
    scan_id = str(uuid.uuid4())
    record_scan_start(scan_id, config.target)
    async def run():
        async with httpx.AsyncClient() as client:
            seen: set = set()
            async def progress(info: ResourceInfo):
                update_scan_progress(scan_id, info)
                record_scan_result(scan_id, info)
            # Fetch sitemap and robots links first
            sitemap_links = await fetch_sitemap_links(config.target, client)
            robots_links = await fetch_robots_links(config.target, client)
            for url in set(sitemap_links + robots_links):
                if url not in seen and len(seen) < config.max_urls:
                    await _crawl(url, config, client, seen, 0, progress)
            # Start crawling the root page
            await _crawl(config.target, config, client, seen, 0, progress)
    background_tasks.add_task(run)
    return scan_id
