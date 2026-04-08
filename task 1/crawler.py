import os
import requests
import time
import bs4
from urllib.parse import urljoin, urlparse
from config import *

class Crawler:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.visited = set()

        self.queue = [self.start_url]
        self.page_id = 1
        self.index_lines = []

    def crawl(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        while self.queue and self.page_id < MAX_PAGES:
            url = self.queue.pop(0)

            if url in self.visited:
                continue

            try:
                print(f"[{self.page_id}] Downloading: {url}")
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }

                response = requests.get(url, headers=headers, timeout=5)

                if response.status_code != 200:
                    continue

                html = response.text

                filename = f"{self.page_id}.txt"
                filepath = os.path.join(OUTPUT_DIR, filename)

                with open(filepath, 'w', encoding="utf-8") as f:
                    f.write(html)

                self.index_lines.append(f"{self.page_id} {url}\n")

                self.visited.add(url)
                self.page_id += 1

                self.parse_urls(url, html)
                time.sleep(DELAY)

            except Exception as e:
                print(f"Error: {e}")
                continue

        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.writelines(self.index_lines)

        print("\nDone!")
        print(f"Downloaded pages: {self.page_id - 1}")


    def parse_urls(self, url: str, html: str):
        soup = bs4.BeautifulSoup(html, "html.parser")

        for link in soup.find_all("a", href = True):
            full_url = urljoin(url, link["href"])

            if full_url not in self.visited:
                self.queue.append(full_url)

    def is_valid_url(self, url: str):
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        if ALLOWED_DOMAIN not in parsed.netloc:
            return False

        if any(url.endswith(ext) for ext in [
            ".jpg", ".png", ".gif", ".svg",
            ".css", ".js", ".pdf", ".zip"
        ]):
            return False

        return True


        
