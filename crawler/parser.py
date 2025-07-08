import logging
from bs4 import BeautifulSoup
from typing import List, Optional
from urllib.parse import urljoin

from config.settings import BASE_URL
from crawler.models import NewsItem


class HNParser:
    def __init__(self):
        self.logger = logging.getLogger("hn_parser")

    def _parse_news_row(self, row) -> Optional[NewsItem]:
        """Parsing a single line of news."""
        try:
            title_elem = row.select_one('.titleline a')
            if not title_elem:
                return None

            title = title_elem.text.strip()
            url = title_elem['href']
            if not url.startswith(('http:', 'https:')):
                url = urljoin(BASE_URL, url)

            item_id = row.get('id', '')
            if not item_id:
                self.logger.warning("No ID found for news row")
                return None

            meta_row = row.find_next_sibling('tr')
            score = int(getattr(meta_row.select_one('.score'), 'text', '0').replace(' points', ''))
            author = getattr(meta_row.select_one('.hnuser'), 'text', 'anonymous')
            comments_url = urljoin(BASE_URL, f"item?id={item_id}")

            return NewsItem(
                id=item_id,
                title=title,
                url=url,
                score=score,
                comments_url=comments_url,
                author=author
            )
        except Exception as e:
            self.logger.error(f"Failed to parse news row: {e}")
            return None

    def parse_news_page(self, html: str) -> List[NewsItem]:
        """Extracts all news from the HN homepage."""
        soup = BeautifulSoup(html, 'lxml')
        rows = soup.select('tr.athing')
        news_items = []

        for row in rows:
            item = self._parse_news_row(row)
            if item:
                news_items.append(item)

        self.logger.info(f"Parsed {len(news_items)} news items")
        return news_items

    def parse_comment_links(self, html: str) -> List[str]:
        """Extracts all external links from comments."""
        soup = BeautifulSoup(html, 'lxml')
        links = []

        for comment in soup.select('.commtext'):
            for a in comment.find_all('a', href=True):
                href = a['href']
                if not href.startswith(('item?id', 'reply?', BASE_URL)):
                    links.append(href)

        self.logger.info(f"Found {len(links)} external links in comments")
        return links
