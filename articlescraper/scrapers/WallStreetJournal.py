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
    soup: BeautifulSoup = BeautifulSoup(article.text, 'html.parser')
    title: str = soup.find('h1', {'itemprop': 'headline'}).text.strip()
    description: str = soup.find(
        'h2', {'itemprop': 'description'}).text.strip()
    content: str = soup.find(
        'div', {'class': 'wsj-snippet-body'}).text.strip()
    author: str = soup.find('a', {'class': 'author-name'}).text.strip()
    date: str = soup.find('time').text.strip()
    return Article(title, description, content, author, date, link)


class WSJ(WebScraper):
    '''This class represents the WallStreetJournal scraper.'''

    def __str__(self) -> str:
        '''This method returns a string that represents the object.'''
        return str('<WSJ_object>')

    def __repr__(self) -> str:
        '''This method returns a string that represents the object.'''
        return str('<WSJ_object>')

    def load_feeds(self, mutex) -> None:
        '''This method loads the feeds from all of WallStreetJournal, using the default links.'''
        super().load_feeds(mutex, pages, "en")
