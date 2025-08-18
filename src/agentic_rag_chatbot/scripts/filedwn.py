import asyncio
from crawl4ai.async_configs import BrowserConfig, AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig
import os
from pathlib import Path

async def download_multiple_files(url: str, download_path: str):
    config = BrowserConfig(accept_downloads=True, downloads_path=download_path)
    async with AsyncWebCrawler(config=config) as crawler:
        run_config = CrawlerRunConfig(
            js_code="""
                const downloadLinks = document.querySelectorAll('a[download]');
                for (const link of downloadLinks) {
                    link.click();
                    // Delay between clicks
                    await new Promise(r => setTimeout(r, 2000));  
                }
            """,
            wait_for=10  # Wait for all downloads to start
        )
        result = await crawler.arun(url=url, config=run_config)

        if result.downloaded_files:
            print("Downloaded files:")
            for file in result.downloaded_files:
                print(f"- {file}")
        else:
            print("No files downloaded.")

# Usage
download_path = os.path.join(Path.home(), ".crawl4ai", "downloads")
os.makedirs(download_path, exist_ok=True)

asyncio.run(download_multiple_files("https://www.python.org/downloads/windows/", download_path))
