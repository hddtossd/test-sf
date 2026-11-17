import re
from urllib.parse import urljoin, urlparse

def _is_same_domain(base: str, url: str) -> bool:
    base_netloc = urlparse(base).netloc.lower()
    url_netloc = urlparse(url).netloc.lower()
    return base_netloc == url_netloc or url_netloc.endswith('.' + base_netloc)

def extract_links(html: str, base_url: str) -> list:
    """Return a list of absolute URLs that are internal to ``base_url``.

    Very simple regex‑based extraction; for production use a proper HTML parser.
    """
    # Find href attributes
    hrefs = re.findall(r'href\s*=\s*"([^"]+)"', html, flags=re.IGNORECASE)
    links = []
    for href in hrefs:
        # Resolve relative URLs
        abs_url = urljoin(base_url, href)
        if _is_same_domain(base_url, abs_url):
            links.append(abs_url.split('#')[0])  # drop fragment
    return list(dict.fromkeys(links))  # dedupe while preserving order
