'''Questo modulo implementa una superclasse per tutti i moduli di scraping.'''
from modules.Article import Article
from modules.Feed import Feed
from feedparser import parse


class WebScraper:
    '''Questa classe rappresenta il WebScraper generico.'''
    def __init__(self) -> None:
        '''Questo è il costruttore della classe.'''
        self.feeds: list[Feed] = []
        self.articles_history: list[Article] = []

    def __str__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<WebScraper_object>')

    def __repr__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<WebScraper_object>')

    def _parse_page(self, page: str, lang: str = "it") -> None:
        '''Questo metodo ritorna i link parsati.'''
        feed = parse(page)
        for entry in feed['entries']:
            self.feeds.append(Feed(entry['link'], entry['title'], lang))

    def fetch_all(self) -> list[Feed]:
        '''Questo metodo ritorna i feed già salvati e parsati nell'oggetto.'''
        return self.feeds