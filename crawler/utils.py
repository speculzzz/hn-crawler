import hashlib
from urllib.parse import urlparse


def generate_id(url: str) -> str:
    """Generate ID from URL"""
    return hashlib.md5(url.encode()).hexdigest()[:8]

def is_internal_url(url: str) -> bool:
    """Check the internal HN link"""
    return urlparse(url).netloc.endswith('ycombinator.com')
