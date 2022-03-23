'''
This module implements the class SearchAutoCompletionBox,
which takes care of the visualization of the search autocompletion box.
'''
import npyscreen
from articlescraper.scrapers.base.Feed import Feed
from articlescraper.NLP import get_affine_feeds


class AutoCompletionBox(npyscreen.Autocomplete):
    '''This class implements an autocompletion box.'''

    def auto_complete(self, _):
        '''This method handles the autocompletion of articles functionality.'''
        feeds_list: list[str] = []
        feeds: list[Feed] = self.find_parent_app().feeds
        scraper: str = self.find_parent_app().browser.website_box.value
        if scraper.strip().lower() != "all" and scraper.strip().lower() != "":
            feeds = [feed for feed in feeds if scraper.strip().lower() in feed.scraper.strip().lower()]
        search: str = self.value.strip()
        if search != "":
            entire_feeds_list = get_affine_feeds(search, feeds)
            feeds_list = [feed.title for feed in entire_feeds_list]
        else:
            feeds_list = [feed.title for feed in feeds]
        if len(feeds_list) == 0:
            self.value = ""
            self.cursor_position = 0
            return
        if len(feeds_list) == 1:
            self.value = feeds_list[0]
            self.cursor_position = len(self.value)
            return
        self.value = feeds_list[self.get_choice(feeds_list)]
        self.cursor_position = len(self.value)


class SearchAutoCompletionBox(npyscreen.TitleFilename):
    '''This is a wrapper class for the personalized autocompletion box.'''
    _entry_type = AutoCompletionBox
