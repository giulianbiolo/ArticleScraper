'''This module handles the search logic.'''
from re import sub as re_sub
from Levenshtein import ratio as Levenshtein_ratio
from articlescraper.scrapers.base.Feed import Feed


def get_affine_feeds(query_title: str, feeds: list[Feed]) -> list[Feed]:
    '''This method returns the feeds that are affine to the query.'''
    query_title = prettify_text(query_title.lower())
    feeds.sort(key=lambda feed: calc_highest_token_score(
        query_title, prettify_text(feed.title.lower())), reverse=True)
    return feeds


def calc_highest_token_score(query_title: str, feed_title: str) -> float:
    '''This method calculates the highest token score.'''
    tokens_query_title = query_title.split(" ")
    tokens_feed_title = feed_title.split(" ")
    token_score_overall: float = 0.0
    for token_query_title in tokens_query_title:
        for token_feed_title in tokens_feed_title:
            token_score_overall += Levenshtein_ratio(
                token_query_title, token_feed_title)
    return token_score_overall


def prettify_text(text: str) -> str:
    '''This method prettifies the text.'''
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
