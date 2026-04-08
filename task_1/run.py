from crawler import Crawler
from config import START_URL

if __name__ == "__main__":
    crawler = Crawler(START_URL)
    crawler.crawl()