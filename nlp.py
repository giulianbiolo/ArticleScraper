'''Questo file gestisce la logica di ricerca di articoli.'''
from re import sub as re_sub
from Levenshtein import ratio as Levenshtein_ratio
from modules.Feed import Feed


def get_affine_feeds(query_title: str, feeds: list[Feed]) -> list[Feed]:
    '''Questo metodo ritorna i feed attinenti osservando la vicinanza al titolo.'''
    query_title = prettify_text(query_title.lower())
    feeds.sort(key=lambda feed: calc_highest_token_score(
        query_title, prettify_text(feed.title.lower())), reverse=True)
    return feeds


def calc_highest_token_score(query_title: str, feed_title: str) -> float:
    '''Questo metodo calcola il miglior score di affinità tra i token del titolo.'''
    tokens_query_title = query_title.split(" ")
    tokens_feed_title = feed_title.split(" ")
    token_score_overall: float = 0.0
    for token_query_title in tokens_query_title:
        for token_feed_title in tokens_feed_title:
            token_score_overall += Levenshtein_ratio(
                token_query_title, token_feed_title)
    return token_score_overall


def prettify_text(text: str) -> str:
    '''Questo metodo ritorna una stringa formattata per la visualizzazione.'''
    # remove special escapes \n, \t, \r
    text = re_sub(r"\\[tr]", " ", text)
    # replace all multiple spaces with single space
    text = re_sub(r"\s{2,}", " ", text)
    text = text.strip()
    # We want to remove all special characters
    whitelist_characters: list[str] = [
        ' ', '.', ',', "'", '!', '?', ':', ';', '-', '_', '+', '=',
        '*', '%', '$', '#', '@', '&', '^', '/', '<', '>', '|', '{',
        '}', '[', ']', '(', ')'
    ]
    return "".join(char for char in text if char.isalnum() or char in whitelist_characters)
