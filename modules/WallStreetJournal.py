'''Questo è il modulo che gestisce lo scraping di wsj.com.'''
import requests
from modules.Article import Article
import feedparser
from bs4 import BeautifulSoup
import Levenshtein


pages: list[str] = [
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",                     # World
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",                   # Markets
    "https://feeds.a.dj.com/rss/RSSWSJD.xml",                          # Technology
    "https://feeds.a.dj.com/rss/RSSOpinion.xml",                       # Opinion
    "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",                 # Business
    "https://feeds.a.dj.com/rss/RSSLifestyle.xml",                     # Lifestyle
]


class WSJ:
    def __init__(self) -> None:
        '''Questo è il costruttore della classe.'''
        self.feeds: list[tuple(str, str)] = []  # (link, titolo)
        for page in pages:
            self._parse_page(page)
        self.articles_history: list[Article] = []

    def __str__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<WSJ_object>')

    def __repr__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<WSJ_object>')

    def _parse_page(self, page) -> None:
        '''Questo metodo ritorna i link parsati.'''
        feed = feedparser.parse(page)
        for entry in feed['entries']:
            self.feeds.append((entry['link'], entry['title']))

    def load_article(self, link: str) -> Article:
        '''Questo metodo ritorna un articolo.'''
        article: str = requests.get(link.strip(), headers={
                                    'User-Agent': 'Custom'})
        soup: BeautifulSoup = BeautifulSoup(article.text, 'html.parser')
        title: str = soup.find(
            'h1', {'class': 'wsj-article-headline'}).text.strip()
        description: str = soup.find('h2', {'class': 'sub-head'}).text.strip()
        content: str = soup.find(
            'div', {'class': 'wsj-snippet-body'}).text.strip()
        author: str = soup.find('a', {'class': 'author-name'}).text.strip()
        date: str = soup.find('time').text.strip()
        self.articles_history.append(
            Article(title, description, content, author, date, link))
        return self.articles_history[-1]

    def find_from_title(self, query_title: str) -> list[tuple]:
        '''Questo metodo ritorna i link che contengono un determinato titolo.'''
        feeds: list[tuple] = []
        for link, title in self.feeds:
            if Levenshtein.ratio(query_title, title) > 0.7:
                feeds.append((link, title))
            for word in title.split(' '):
                if Levenshtein.ratio(query_title, word) > 0.7:
                    feeds.append((link, title))
        return feeds


def test() -> None:
    '''Questo è il metodo di test.'''
    wsj: WSJ = WSJ()
    parsed_feeds = wsj.feeds
    print("Articoli Di Giornale: " + str(len(parsed_feeds)))
    articolo: Article = wsj.load_article(parsed_feeds[0][0])
    print(articolo)  # Stampa solo il titolo così
    articolo.print()  # Stampa tutto l'articolo
    return


if __name__ == '__main__':
    test()