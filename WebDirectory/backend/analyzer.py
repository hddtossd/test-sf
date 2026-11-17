from dataclasses import dataclass
from typing import Optional

@dataclass
class ResourceInfo:
    url: str
    status_code: int
    content_type: str
    body: Optional[bytes] = None
    discovery_method: str = "unknown"

def analyze_response(url: str, response) -> ResourceInfo:
    """Create a ResourceInfo from an httpx.Response.
    The ``discovery_method`` is to be set by the caller.
    """
    ct = response.headers.get("content-type", "").split(";")[0].strip()
    body = response.content if ct.startswith("text") else None
    return ResourceInfo(
        url=url,
        status_code=response.status_code,
        content_type=ct,
        body=body,
        discovery_method="crawl",  # placeholder, will be overridden where appropriate
    )
