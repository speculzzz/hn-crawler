from setuptools import find_packages, setup


setup(
    name="hn-crawler",
    version="0.1.0",
    description="Hacker News crawler",
    url="https://github.com/speculzzz/hn-crawler",
    author="speculzzz",
    author_email="speculzzz@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="OTUS homework 16",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.12",
    license="MIT",
    install_requires=[
        "asyncio>=3.4.3",
        "aiohttp>=3.12.13",
        "aiosqlite>=0.21.0",
        "pydantic>=2.11.7",
        "beautifulsoup4>=4.13.4",
        "lxml>=6.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=8.4.1",
            "pytest-cov>=6.2.1",
            "pytest-asyncio>=1.0.0"
        ],
    },
    entry_points={
        "console_scripts": [
            "hn-crawler=crawler.main:main",
        ],
    },
)
