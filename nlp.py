from modules.Feed import Feed
import spacy


def get_affine_feeds(query_title: str, feeds: list[Feed]) -> list[Feed]:
    '''Questo metodo ritorna i feed attinenti al testo ricercato, osservando la vicinanza al titolo.'''
    affine_feeds: list[Feed] = []
    # Dividiamo feeds in due liste divise per lingua
    it_feeds: list[Feed] = []
    en_feeds: list[Feed] = []
    for feed in feeds:
        if feed.lang == "it":
            it_feeds.append(feed)
        else:
            en_feeds.append(feed)
    # Ricerca in italiano
    nlp = spacy.load("it_core_news_sm")
    query_title_dec = nlp(query_title)
    for feed in it_feeds:
        feed_title_dec = nlp(feed.title)
        if feed_title_dec.similarity(query_title_dec) > 0.8:
            affine_feeds.append(feed)
    # Ricerca in inglese
    nlp = spacy.load("en_core_web_sm")
    query_title_dec = nlp(query_title)
    for feed in en_feeds:
        feed_title_dec = nlp(feed.title)
        if feed_title_dec.similarity(query_title_dec) > 0.8:
            affine_feeds.append(feed)
    return affine_feeds


def prettify_text(text: str, lang="it") -> str:
    '''Questo metodo ritorna una stringa formattata per la visualizzazione.'''
    if lang == "it":
        nlp = spacy.load("it_core_news_sm")
    else:
        nlp = spacy.load("en_core_web_sm")
    text_dec = nlp(text)
    text_dec = [sentence.text.strip() for sentence in text_dec.sents]
    return "\n".join(text_dec)
