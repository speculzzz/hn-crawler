import aiohttp
import asyncio
from typing import Optional

from config.settings import BASE_URL, REQUEST_TIMEOUT, USER_AGENT, MAX_RETRIES, MAX_CONCURRENT_REQUESTS
from crawler.models import FetchResult


class PageFetcher:
    def __init__(self):
        self.session = None
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        self.request_count = 0

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *exc):
        await self.close()

    async def start(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers={'User-Agent': USER_AGENT}
            )

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def fetch(self, url: str, retries: int = MAX_RETRIES) -> FetchResult:
        """Get a page with retries"""
        if not self.session:
            await self.start()

        self.request_count += 1

        async with self.semaphore:
            last_exception = None

            for attempt in range(retries):
                try:
                    async with self.session.get(url) as response:
                        if response.status >= 400:
                            raise FetchError(
                                url=str(response.url),
                                status=response.status,
                                message=f"HTTP Error {response.status}"
                            )
                        content = await response.text()
                        return FetchResult(
                            content=content,
                            status=response.status,
                            url=str(response.url)
                        )
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    last_exception = e
                    if attempt < retries - 1:
                        await asyncio.sleep(1 * (attempt + 1))

            raise FetchError(
                url=url,
                status=getattr(last_exception, 'status', None),
                message=f"Failed after {retries} attempts: {str(last_exception)}"
            )

    async def fetch_hn_page(self, page: str = "") -> str:
        """Get the Hacker News page """
        url = f"{BASE_URL}/{page}"
        result = await self.fetch(url)
        if result.status == 200:
            return result.content
        raise FetchError(f"HN returned {result.status} for {url}")


class FetchError(Exception):
    def __init__(self, url: str, status: Optional[int] = None, message: str = ""):
        self.url = url
        self.status = status
        self.message = message
        super().__init__(f"{self.status} | {self.url} | {self.message}")

