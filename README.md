# Hacker News Crawler

## Project Overview
Async web crawler for Hacker News (news.ycombinator.com) with data storage.  
It is a part of Homework 16 for the OTUS course and is intended for educational purposes.

## Features

- 🕷️ Async crawling using `aiohttp`
- 📰 Parsing top news stories and comments
- 💾 SQLite storage with `aiosqlite`
- ⚙️ Configurable via `settings.py`
- 🔍 Supports both crawling and data querying

## Installation

```bash
git clone https://github.com/speculzzz/hn-crawler.git
cd hn-crawler
pip install -r requirements.txt
```

## Usage
### Run crawler (continuous mode):

```bash
python main.py
```

### Single crawl cycle:

```bash
python main.py --once
```

### Show last 5 saved news:

```bash
python main.py --show 5
```

## Configuration

Edit config/settings.py to adjust:

- Crawl intervals
- Request timeouts
- Concurrent connections
- User agent

## Project Structure

```
hn-crawler/
├── crawler/          # Core logic
│   ├── crawler.py    # The main crawler object
│   ├── fetcher.py    # HTTP client
│   ├── main.py       # Main script
│   ├── models.py     # Models
│   ├── parser.py     # HTML parsing
│   └── storage.py    # Database ops
├── config/           # Settings
└── tests/            # Unit tests
```

## Requirements
- Python 3.12+
- Packages: aiohttp, beautifulsoup4, aiosqlite


## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

- **speculzzz** (speculzzz@gmail.com)

---

Feel free to use it!
