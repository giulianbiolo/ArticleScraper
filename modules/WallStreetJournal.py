'''Questo è il modulo che gestisce lo scraping di wsj.com.'''
import threading
from requests import get as reqget
from bs4 import BeautifulSoup
from modules.Article import Article
from modules.WebScraper import WebScraper


pages: list[str] = [
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",                     # World
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",                   # Markets
    "https://feeds.a.dj.com/rss/RSSWSJD.xml",                          # Technology
    "https://feeds.a.dj.com/rss/RSSOpinion.xml",                       # Opinion
    "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",                 # Business
    "https://feeds.a.dj.com/rss/RSSLifestyle.xml",                     # Lifestyle
]


def is_wsj_article(link: str) -> bool:
    '''Questo metodo ritorna True se l'articolo è di wsj.com.'''
    return link.find('wsj.com') != -1


class WSJ(WebScraper):
    '''Questa classe implementa il webscraper di wsj.com.'''

    def __str__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<WSJ_object>')

    def __repr__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<WSJ_object>')

    def _load_feeds(self) -> None:
        '''Questo metodo carica i feeds.'''
        threads = []
        for page in pages:
            threads.append(threading.Thread(
                target=self._parse_page, args=(page,)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def _parse_page(self, page) -> None:
        '''Questo metodo ritorna i link parsati.'''
        super()._parse_page(page, "en")

    def load_article(self, link: str) -> Article:
        '''Questo metodo ritorna un articolo.'''
        article: str = reqget(link.strip(), headers={
                                    'User-Agent': 'Custom'})
        soup: BeautifulSoup = BeautifulSoup(article.text, 'html.parser')
        title: str = soup.find('h1', {'itemprop': 'headline'}).text.strip()
        description: str = soup.find(
            'h2', {'itemprop': 'description'}).text.strip()
        content: str = soup.find(
            'div', {'class': 'wsj-snippet-body'}).text.strip()
        author: str = soup.find('a', {'class': 'author-name'}).text.strip()
        date: str = soup.find('time').text.strip()
        self.articles_history.append(
            Article(title, description, content, author, date, link))
        return self.articles_history[-1]
