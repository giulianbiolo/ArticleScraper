'''This module implements a superclass for all of the scraping modules.'''
from threading import Thread, Lock
from requests import get
from speedparser3 import parse
from articlescraper.scrapers.base.Article import Article
from articlescraper.scrapers.base.Feed import Feed


class WebScraper:
    '''This class represents a generic WebScraper.'''

    def __init__(self, mutex: Lock) -> None:
        '''This is the constructor of the class.'''
        mutex.acquire()
        self.loaded: bool = False
        mutex.release()
        self.feeds: list[Feed] = []
        self.articles_history: list[Article] = []

    def __str__(self) -> str:
        '''This method returns a string that represents the object.'''
        return str('<WebScraper_Object>')

    def __repr__(self) -> str:
        '''This method returns a string that represents the object.'''
        return str('<WebScraper_Object>')

    def _parse_page(self, page: str, lang: str = "en", scraper_name: str = "unknown") -> None:
        '''This method parses a single page.'''
        xmldoc: str = get(page).text
        feed = parse(xmldoc.encode("utf-8"))
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
        mutex.acquire()
        self.loaded = True
        mutex.release()

    def fetch_all(self) -> list[Feed]:
        '''This method returns all the already fetched feeds.'''
        return self.feeds if self.loaded else None
