'''This module takes care of scraping the WallStreetJournal website.'''
from requests import get as reqget
from bs4 import BeautifulSoup
from articlescraper.scrapers.base import Article
from articlescraper.scrapers.base import WebScraper


pages: list[str] = [
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",                     # World
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",                   # Markets
    "https://feeds.a.dj.com/rss/RSSWSJD.xml",                          # Technology
    "https://feeds.a.dj.com/rss/RSSOpinion.xml",                       # Opinion
    "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",                 # Business
    "https://feeds.a.dj.com/rss/RSSLifestyle.xml",                     # Lifestyle
]


def is_wsj_article(link: str) -> bool:
    '''This method returns True if the given link is a WSJ article.'''
    return link.find('wsj.com') != -1


def load_article(link: str) -> Article:
    '''This method loads the article content given the link.'''
    article: str = reqget(link.strip(), headers={
        'User-Agent': 'Custom'})
    soup: BeautifulSoup = BeautifulSoup(article.text, 'lxml')
    title: str = soup.find('h1').text.strip()
    description: str = soup.find('h2').text.strip()
    content: str = ""
    try:
        content = soup.find(
            'div', {'class': 'wsj-snippet-body'}).text.strip()
    except:
        try:
            content = soup.find_all('section')[1].text.strip()
        except:
            try:
                content = soup.find(
                    'div', {'id': 'wsj-article-wrap'}).findAll('p')
                for p in content:
                    content += p.text.strip()
            except:
                pass
    author: str = ""
    try:
        author = soup.find('a', {'class': 'author-name'}).text.strip()
    except:
        try:
            author = soup.find('span', {'class': 'author-name'}).text.strip()
        except:
            pass
    date: str = soup.find('time').text.strip()
    if content == "":
        content = description
        description = ""
    return Article(title, description, content, author, date, link)


class WSJ(WebScraper):
    '''This class represents the WallStreetJournal scraper.'''

    def load_feeds(self, mutex) -> None:
        '''This method loads the feeds from all of WallStreetJournal, using the default links.'''
        super().load_feeds(mutex, pages, "en", "WallStreetJournal")
