'''Questo modulo gestisce alcuni funzioni di utilità.'''
from modules.Article import Article
from modules.Ansa import is_ansa_article
from modules.WallStreetJournal import is_wsj_article
from nlp import prettify_text


def load_article_file(filename: str) -> tuple[str, str, str]:
    '''Questo metodo carica un articolo da un file.'''
    title: str = ""
    description: str = ""
    body: str = ""
    with open(filename, "rb") as file:
        raw_data: str = file.read().decode("utf-8")
        title = raw_data.split("\n")[0].strip()
        description = raw_data.split("\n")[1].strip()
        body = "\n".join(raw_data.split("\n")[2:]).strip()
    return title, description, prettify_text(body)


def load_article(link: str, lang: str = "it") -> tuple[str, str, str]:
    '''Questo metodo carica un articolo dal link.'''
    title: str = ""
    description: str = ""
    body: str = ""
    article: Article = None
    if is_ansa_article(link):
        from modules.Ansa import Ansa
        ansa: Ansa = Ansa()
        article = ansa.load_article(link)
    elif is_wsj_article(link):
        from modules.WallStreetJournal import WSJ
        wsj: WSJ = WSJ()
        article = wsj.load_article(link)
    if article is not None:
        title = article.title
        description = article.description
        body = prettify_text(article.content, lang)
    return title, description, body
