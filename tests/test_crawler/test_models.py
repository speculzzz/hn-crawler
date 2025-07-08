from crawler.models import NewsItem


def test_news_item_creation():
    item = NewsItem(
        id="123",
        title="Test",
        url="http://example.com",
        score=10,
        author="user",
        comments_url="/item?id=123"
    )
    assert item.domain == "example.com"
