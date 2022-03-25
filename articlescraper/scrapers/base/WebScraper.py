'''This module implements a superclass for all of the scraping modules.'''
from threading import Thread, Lock
from requests import get as reqget
from speedparser3 import parse
from articlescraper.scrapers.base.Article import Article
from articlescraper.scrapers.base.Feed import Feed


class WebScraper:
    '''This class represents a generic WebScraper.'''

    def __init__(self, mutex: Lock) -> None:
        '''This is the constructor of the class.'''
        with mutex:
            self.loaded: bool = False
        self.feeds: list[Feed] = []
        self.articles_history: list[Article] = []

    def _parse_page(self, page: str, lang: str = "en", scraper_name: str = "unknown") -> None:
        '''This method parses a single page.'''
        xmldoc: str = reqget(page).text
        feed = parse(xmldoc.encode("utf-8"), clean_html=False)
        for entry in feed['entries']:
            self.feeds.append(Feed(entry['link'], entry['title'], lang, scraper_name))

    def load_feeds(self, mutex, pages: list[str], lang: str = "en", scraper_name: str = "unknown") -> None:
        '''This method loads the feeds from the given pages.'''
        threads = []
        for page in pages:
            threads.append(Thread(
                target=self._parse_page, args=(page, lang, scraper_name)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        with mutex:
            self.loaded = True

    def fetch_all(self) -> list[Feed]:
        '''This method returns all the already fetched feeds.'''
        return self.feeds if self.loaded else None
