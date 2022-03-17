'''Questo è il modulo che gestisce lo scraping di Ansa.it.'''
import requests
from modules.Article import Article
import feedparser
from bs4 import BeautifulSoup
import Levenshtein

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


class Ansa:
    def __init__(self) -> None:
        '''Questo è il costruttore della classe.'''
        self.feeds: list[tuple(str, str)] = []  # (link, titolo)
        for page in pages:
            self._parse_page(page)
        self.articles_history: list[Article] = []

    def __str__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<Ansa_object>')

    def __repr__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str('<Ansa_object>')

    def _parse_page(self, page) -> None:
        '''Questo metodo ritorna i link parsati.'''
        feed = feedparser.parse(page)
        for entry in feed['entries']:
            self.feeds.append((entry['link'], entry['title']))

    def load_article(self, link: str) -> Article:
        '''Questo metodo ritorna il contenuto dell'articolo.'''
        article = requests.get(link.strip(), headers={'User-Agent': 'Custom'})
        soup = BeautifulSoup(article.text, 'html.parser')
        title: str = soup.find('h1', {'class': 'news-title'}).text.strip()
        description: str = soup.find('h2', {'class': 'news-stit'}).text.strip()
        content: str = soup.find('div', {'class': 'news-txt'}).text.strip()
        author: str = soup.find('span', {'class': 'news-author'}).text.strip()
        unparsed_date: str = soup.find('time').text.strip()
        date: str = (unparsed_date[:-6] + " " + unparsed_date[-6:]).strip()
        self.articles_history.append(
            Article(title, description, content, author, date, link))
        return self.articles_history[-1]

    def find_from_title(self, query_title: str) -> list[tuple]:
        '''Questo metodo, dato un titolo, trova gli articoli più attinenti.'''
        # TODO: Implementare una funzione che trova gli articoli più attinenti migliore
        feeds: list[tuple] = []
        for link, title in self.feeds:
            if Levenshtein.ratio(query_title, title) > 0.7:
                feeds.append((link, title))
            for word in title.split(' '):
                if Levenshtein.ratio(query_title, word) > 0.7:
                    feeds.append((link, title))
        return feeds

    def find_all(self) -> list[tuple]:
        '''Questo metodo, dato un titolo, trova gli articoli più attinenti.'''
        return self.feeds


def test() -> None:
    '''Questo è il metodo di test.'''
    ansa: Ansa = Ansa()
    parsed_feeds = ansa.feeds
    print("Articoli Di Giornale: " + str(len(parsed_feeds)))
    articolo: Article = ansa.load_article(parsed_feeds[0][0])
    print(articolo)  # Stampa solo il titolo così
    articolo.print()  # Stampa tutto l'articolo
    return


if __name__ == '__main__':
    test()
