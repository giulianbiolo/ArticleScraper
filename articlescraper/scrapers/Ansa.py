'''Questo è il modulo che gestisce lo scraping di Ansa.it.'''
from requests import get as reqget
from bs4 import BeautifulSoup
from articlescraper.scrapers.base import Article
from articlescraper.scrapers.base import WebScraper


pages: list[str] = [
    'https://www.ansa.it/sito/ansait_rss.xml',                         # Homepage
    'https://www.ansa.it/sito/notizie/cronaca/cronaca_rss.xml',        # Cronaca
    'https://www.ansa.it/sito/notizie/politica/politica_rss.xml',      # Politica
    'https://www.ansa.it/sito/notizie/economia/economia_rss.xml',      # Economia
    'https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml',            # Mondo
    'https://www.ansa.it/sito/notizie/sport/calcio/calcio_rss.xml',    # Calcio
    'https://www.ansa.it/sito/notizie/sport/sport_rss.xml',            # Sport
    'https://www.ansa.it/sito/notizie/cultura/cinema/cinema_rss.xml',  # Cinema
    'https://www.ansa.it/sito/notizie/cultura/cultura_rss.xml',        # Cultura
    'https://www.ansa.it/sito/notizie/tecnologia/tecnologia_rss.xml',  # Tecnologia
    'https://www.ansa.it/sito/notizie/topnews/topnews_rss.xml',        # Ultima Ora
    'https://www.ansa.it/europa/notizie/rss.xml',                      # Europa
]


def is_ansa_article(link: str) -> bool:
    '''Questo metodo ritorna True se l'articolo è di Ansa.'''
    return link.find('ansa.it') != -1


def load_article(link: str) -> Article:
    '''Questo metodo ritorna il contenuto dell'articolo.'''
    article = reqget(link.strip(), headers={'User-Agent': 'Custom'})
    soup = BeautifulSoup(article.text, 'html.parser')
    title: str = soup.find('h1', {'class': 'news-title'}).text.strip()
    description: str = soup.find('h2', {'class': 'news-stit'}).text.strip()
    content: str = soup.find('div', {'class': 'news-txt'}).text.strip()
    author: str = soup.find('span', {'class': 'news-author'}).text.strip()
    unparsed_date: str = soup.find('time').text.strip()
    date: str = (unparsed_date[:-6] + " " + unparsed_date[-6:]).strip()
    return Article(title, description, content, author, date, link)


class Ansa(WebScraper):
    '''Questa classe implementa il webscraper di Ansa.it.'''

    def __str__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<Ansa_object>')

    def __repr__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<Ansa_object>')

    def load_feeds(self, mutex) -> None:
        '''Questo metodo carica i feeds.'''
        super().load_feeds(mutex, pages, "it")