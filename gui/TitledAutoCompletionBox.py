'''Questo modulo implementa la classe della finestra di autocompletamento.'''
import npyscreen
from modules.Feed import Feed
from NLP import get_affine_feeds


class AutoCompletionBox(npyscreen.Autocomplete):
    '''Questa classe gestisce il funzionamento dell'autocompletamento degli articoli.'''

    def auto_complete(self, _):
        '''Questo è l'override del metodo che gestisce i feed degli autocompletamenti.'''
        feeds_list: list[str] = []
        feeds: list[Feed] = self.find_parent_app().feeds
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


class TitledAutoCompletionBox(npyscreen.TitleFilename):
    '''Questa è la classe wrapper con testo dell'autocompletamento personalizzato.'''
    _entry_type = AutoCompletionBox
