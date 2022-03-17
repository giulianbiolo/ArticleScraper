from modules.Feed import Feed
import Levenshtein


def get_affine_feeds(query_title: str, feeds: list[Feed]) -> list[Feed]:
    '''Questo metodo ritorna i feed attinenti al testo ricercato, osservando la vicinanza al titolo.'''
    query_title = prettify_text(query_title.lower())
    feeds.sort(key=lambda feed: calc_highest_token_score(query_title, prettify_text(feed.title.lower())), reverse=True)
    return feeds


def calc_highest_token_score(query_title: str, feed_title: str) -> float:
    '''Questo metodo calcola il miglior score di affinità tra i token del titolo.'''
    tokens_query_title = query_title.split(" ")
    tokens_feed_title = feed_title.split(" ")
    token_score_overall: float = 0.0
    for token_query_title in tokens_query_title:
        for token_feed_title in tokens_feed_title:
            token_score_overall += Levenshtein.ratio(token_query_title, token_feed_title)
    return token_score_overall



def prettify_text(text: str) -> str:
    '''Questo metodo ritorna una stringa formattata per la visualizzazione.'''
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    text = text.replace("  ", " ")
    text = text.strip()
    return text
