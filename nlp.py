from modules.Feed import Feed
import Levenshtein


def get_affine_feeds(query_title: str, feeds: list[Feed]) -> list[Feed]:
    '''Questo metodo ritorna i feed attinenti al testo ricercato, osservando la vicinanza al titolo.'''
    query_title = query_title.lower()
    query_title = prettify_text(query_title)
    affine_feeds: list[Feed] = []
    for feed in feeds:
        if Levenshtein.ratio(query_title, prettify_text(feed.title.lower())) > 0.8:
            affine_feeds.append(feed)
            continue
        for word in prettify_text(feed.title.lower()).split():
            if Levenshtein.ratio(query_title, word) > 0.8:
                affine_feeds.append(feed)
                break
    return affine_feeds


def prettify_text(text: str) -> str:
    '''Questo metodo ritorna una stringa formattata per la visualizzazione.'''
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    text = text.replace("  ", " ")
    text = text.strip()
    return text
