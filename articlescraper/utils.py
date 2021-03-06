'''This module handles some utility functions.'''
from articlescraper.NLP import prettify_text
from articlescraper.scrapers.base.Article import Article
from articlescraper.scrapers.Ansa import is_ansa_article
from articlescraper.scrapers.WallStreetJournal import is_wsj_article
from articlescraper.scrapers.NewYorkTimes import is_nyt_article


def load_article_file(filename: str) -> tuple[str, str, str]:
    '''This method loads the article given a filename.'''
    title: str = ""
    description: str = ""
    body: str = ""
    with open(filename, "rb") as file:
        raw_data: str = file.read().decode("utf-8")
        title = raw_data.split("\n")[0].strip()
        description = raw_data.split("\n")[1].strip()
        body = "\n".join(raw_data.split("\n")[2:]).strip()
    return title, description, prettify_text(body)


def load_article(link: str) -> tuple[str, str, str]:
    '''This method loads the article given the link.'''
    title: str = ""
    description: str = ""
    body: str = ""
    article: Article = None
    if is_ansa_article(link):
        from articlescraper.scrapers.Ansa import load_article as ansa_load_article
        article = ansa_load_article(link)
    elif is_wsj_article(link):
        from articlescraper.scrapers.WallStreetJournal import load_article as wsj_load_article
        article = wsj_load_article(link)
    elif is_nyt_article(link):
        from articlescraper.scrapers.NewYorkTimes import load_article as nyt_load_article
        article = nyt_load_article(link)
    if article is not None:
        title = article.title
        description = article.description
        body = prettify_text(article.content)
    return title, description, body
