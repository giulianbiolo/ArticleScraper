'''This module takes care of scraping the NewYorkTimes website.'''
from requests import get as reqget
from bs4 import BeautifulSoup
from articlescraper.scrapers.base import Article
from articlescraper.scrapers.base import WebScraper


pages: list[str] = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",          # World
    "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",             # U.S.
    "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",       # Business
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",     # Technology
    "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",         # Sports
    "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",        # Science
    "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",         # Health
]


def is_nyt_article(link: str) -> bool:
    '''This method returns True if the given link is a NYT article.'''
    return link.find('nytimes.com') != -1


def load_article(link: str) -> Article:
    '''This method loads the article content given the link.'''
    article: str = reqget(link.strip(), headers={
        'User-Agent': 'Custom'})
    soup: BeautifulSoup = BeautifulSoup(article.text, 'lxml')
    title: str = soup.find('h1', {'data-testid': 'headline'}).text.strip()
    description: str = soup.find('p', {'id': 'article-summary'}).text.strip()
    content: str = ""
    try:
        content = soup.find(
            'section', {'name': 'articleBody'}).text.strip()
    except:
        pass
    author: str = ""
    try:
        author = soup.find('span', {'itemprop': 'name'}).text.strip()
    except:
        pass
    date: str = ""
    try:
        date: str = soup.find('time').text.strip()
    except:
        pass
    if content == "":
        content = description
        description = ""
    return Article(title, description, content, author, date, link)


class NYT(WebScraper):
    '''This class represents the NewYorkTimes scraper.'''

    def load_feeds(self, mutex) -> None:
        '''This method loads the feeds from all of NewYorkTimes, using the default links.'''
        super().load_feeds(mutex, pages, "en", "NewYorkTimes")
