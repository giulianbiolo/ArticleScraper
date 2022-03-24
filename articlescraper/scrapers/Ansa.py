'''This module takes care of scraping the Ansa website.'''
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
    '''This method returns True if the given link is an Ansa article.'''
    return link.find('ansa.it') != -1


def load_article(link: str) -> Article:
    '''This method loads the article content given the link.'''
    article = reqget(link.strip(), headers={'User-Agent': 'Custom'})
    soup = BeautifulSoup(article.text, 'lxml')
    title: str = soup.find('h1', {'class': 'news-title'}).text.strip()
    description: str = soup.find('h2', {'class': 'news-stit'}).text.strip()
    content: str = soup.find('div', {'class': 'news-txt'}).text.strip()
    author: str = soup.find('span', {'class': 'news-author'}).text.strip()
    unparsed_date: str = soup.find('time').text.strip()
    date: str = (unparsed_date[:-6] + " " + unparsed_date[-6:]).strip()
    return Article(title, description, content, author, date, link)


class Ansa(WebScraper):
    '''This class represents the Ansa scraper.'''

    def load_feeds(self, mutex) -> None:
        '''This method loads the feeds from all of Ansa, using the default links.'''
        super().load_feeds(mutex, pages, "it", "Ansa")
