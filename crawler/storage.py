import aiosqlite
import logging
from typing import List, Optional, AsyncIterator

from crawler.models import NewsItem


class HNStorage:
    def __init__(self, db_path: str = 'hacker_news.db'):
        self.db_path = db_path
        self.connection: Optional[aiosqlite.Connection] = None
        self.logger = logging.getLogger('hn_storage')

    async def connect(self):
        """Establishing a database connection once"""
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_path)
            await self._init_db()
            self.logger.info("Database connection established")

    async def close(self):
        """Close connection"""
        if self.connection:
            await self.connection.close()
            self.logger.info("Database connection closed")

    async def _init_db(self):
        """Initializing tables"""
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                score INTEGER,
                comments_url TEXT,
                author TEXT,
                domain TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS comment_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                news_id TEXT,
                url TEXT NOT NULL,
                FOREIGN KEY (news_id) REFERENCES news (id)
            )
        ''')
        await self.connection.commit()

    async def save_news_item(self, item: NewsItem) -> bool:
        """Saving the news using an existing connection"""
        try:
            await self.connection.execute(
                '''
                INSERT OR IGNORE INTO news`
                (id, title, url, score, comments_url, author, domain)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (item.id, item.title, item.url, item.score,
                 item.comments_url, item.author, item.domain)
            )
            await self.connection.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error saving news: {e}")
            return False

    async def save_comment_links(self, news_id: str, links: List[str]) -> int:
        """Saving links using an existing connection"""
        if not links:
            return 0

        try:
            await self.connection.execute(
                "DELETE FROM comment_links WHERE news_id = ?",
                (news_id,)
            )

            await self.connection.executemany(
                "INSERT INTO comment_links (news_id, url) VALUES (?, ?)",
                [(news_id, link) for link in links]
            )
            await self.connection.commit()
            return len(links)
        except Exception as e:
            self.logger.error(f"Error saving links: {e}")
            return 0

    async def get_recent_news(self, limit: int = 10) -> AsyncIterator[NewsItem]:
        """Getting the recent news"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM news ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ) as cursor:
                async for row in cursor:
                    yield NewsItem(
                        id=row['id'],
                        title=row['title'],
                        url=row['url'],
                        score=row['score'],
                        comments_url=row['comments_url'],
                        author=row['author'],
                    )
