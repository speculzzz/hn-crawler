import pytest
from crawler.fetcher import PageFetcher


@pytest.fixture
async def fetcher():
    async with PageFetcher() as f:
        yield f


@pytest.fixture
def sample_news_html():
    return """
    <tr class="athing" id="123">
        <td class="title"><span class="titleline"><a href="https://example.com">Test Title</a></span></td>
    </tr>
    <tr>
        <td class="subtext"><span class="score">42 points</span> by <a class="hnuser">user</a></td>
    </tr>
    """
