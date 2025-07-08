import asyncio
import logging

from config.settings import CRAWL_INTERVAL
from crawler.models import NewsItem
from crawler.fetcher import PageFetcher, FetchError
from crawler.parser import HNParser
from crawler.storage import HNStorage


class HNCrawler:
    def __init__(self, interval: int = CRAWL_INTERVAL):
        self.interval = interval
        self.fetcher = PageFetcher()
        self.parser = HNParser()
        self.storage = HNStorage()
        self.seen_ids = set()
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Configure application logger"""
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        return logging.getLogger('hn_crawler')

    async def fetch_top_news(self) -> list[NewsItem]:
        """Fetch current top news from HN front page"""
        self.logger.info("Fetch top news")
        html = await self.fetcher.fetch_hn_page("news")
        return self.parser.parse_news_page(html)

    async def process_comments(self, item: NewsItem) -> list[str]:
        """Extract all links from news comments"""
        self.logger.info("Extract all links from news comments")
        html = await self.fetcher.fetch(item.comments_url)
        return self.parser.parse_comment_links(html.content)

    async def save_results(self, item: NewsItem, links: list[str]) -> None:
        """Save news item and related links to storage"""
        self.logger.info("Save news item and related links to storage")
        self.logger.info(str(item) + f"\nExternal links: {links}")
        try:
            news_saved = await self.storage.save_news_item(item)
            if news_saved:
                links_saved = await self.storage.save_comment_links(item.id, links)
                self.logger.info(f"Saved {links_saved} links for item {item.id}")
            else:
                self.logger.warning(f"News item {item.id} already exists, skipped links")

        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")

    async def _crawl_cycle(self) -> None:
        """Single crawl iteration"""
        try:
            self.logger.debug(f"The main crawler cycle")
            news_items = await self.fetch_top_news()
            for item in news_items:
                if item.id not in self.seen_ids:
                    links = await self.process_comments(item)
                    await self.save_results(item, links)
                    self.seen_ids.add(item.id)
                    self.logger.info(f"Processed: {item.title}")
        except FetchError as e:
            # Too many requests
            if e.status == 429:
                await asyncio.sleep(60)
        except Exception as e:
            self.logger.error(f"Crawl cycle failed: {str(e)}")

    async def run(self, run_once: bool = False) -> None:
        """Main entry point"""
        self.logger.info("Starting Hacker News crawler")
        try:
            await self.storage.connect()
            await self.fetcher.start()

            while True:
                await self._crawl_cycle()
                if run_once:
                    break
                await asyncio.sleep(self.interval)

        finally:
            await self.fetcher.close()
            await self.storage.close()

    async def show_recent_news(self, limit: int = 5):
        """Displays the latest saved news with formatting"""
        try:
            print(f"\nLast {limit} news items:")
            print("-" * 50)

            async for news_item in self.storage.get_recent_news(limit):
                print(str(news_item))
                print("-" * 50)

        except Exception as e:
            self.logger.error(f"Failed to fetch recent news: {e}")
