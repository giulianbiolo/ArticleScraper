'''Questo modulo implementa una superclasse per tutti i moduli di scraping.'''
from threading import Thread, Lock
from feedparser import parse as feedparse
from modules.Article import Article
from modules.Feed import Feed


class WebScraper:
    '''Questa classe rappresenta il WebScraper generico.'''

    def __init__(self, mutex: Lock) -> None:
        '''Questo è il costruttore della classe.'''
        mutex.acquire()
        self.loaded: bool = False
        mutex.release()
        self.feeds: list[Feed] = []
        self.articles_history: list[Article] = []

    def __str__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<WebScraper_Object>')

    def __repr__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<WebScraper_Object>')

    def _parse_page(self, page: str, lang: str = "en") -> None:
        '''Questo metodo ritorna i link parsati.'''
        feed = feedparse(page)
        for entry in feed['entries']:
            self.feeds.append(Feed(entry['link'], entry['title'], lang))

    def load_feeds(self, mutex, pages: list[str], lang: str = "en") -> None:
        '''Questo metodo carica i feeds.'''
        threads = []
        for page in pages:
            threads.append(Thread(
                target=self._parse_page, args=(page, lang)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        mutex.acquire()
        self.loaded = True
        mutex.release()

    def fetch_all(self) -> list[Feed]:
        '''Questo metodo ritorna i feed già salvati e parsati nell'oggetto.'''
        return self.feeds if self.loaded else None
