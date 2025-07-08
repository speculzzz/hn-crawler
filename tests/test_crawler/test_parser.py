import pytest
from crawler.parser import HNParser


@pytest.mark.asyncio
async def test_parse_news_item(sample_news_html):
    parser = HNParser()
    items = parser.parse_news_page(sample_news_html)
    assert items[0].title == "Test Title"
    assert items[0].score == 42
