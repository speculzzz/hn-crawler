from dataclasses import dataclass
from textwrap import shorten


@dataclass(frozen=True)
class NewsItem:
    id: str
    title: str
    url: str
    score: int
    comments_url: str
    author: str

    @property
    def domain(self) -> str:
        """Extract domain from URL"""
        from urllib.parse import urlparse
        return urlparse(self.url).netloc

    def __str__(self) -> str:
        """Pretty print format"""
        title_short = shorten(self.title, width=60, placeholder="...")
        return (
            f"NewsItem(id={self.id}, score={self.score}, author={self.author}\n"
            f"\tTitle: {title_short}\n"
            f"\tURL: {self.url}\n"
            f"\tComments: {self.comments_url}\n"
            f"\tDomain: {self.domain}\n)"
        )


@dataclass
class FetchResult:
    content: str
    status: int
    url: str

    def __str__(self) -> str:
        """Pretty print format"""
        content_preview = shorten(self.content, width=50, placeholder="...")
        return (
            f"FetchResult(status={self.status}, url={self.url}\n"
            f"Content preview: {content_preview})"
        )
