from modules.Feed import Feed
import npyscreen
import Levenshtein


class AutoCompletionBox(npyscreen.Autocomplete):
    '''Questa classe gestisce il funzionamento dell'autocompletamento degli articoli.'''

    def auto_complete(self, _):
        '''Questo è l'override del metodo che gestisce i feed degli autocompletamenti.'''
        feeds_list: list[Feed] = []
        feeds: list[Feed] = self.find_parent_app().feeds
        search: str = self.value.strip().lower()
        if search != "":
            for feed in feeds:
                for word in feed.title.strip().lower().split():
                    # TODO: Migliorare l'algoritmo di ricerca
                    # TODO: f(query_title:str, feeds:list[tuple[link:str,title:str]]) -> affine_feeds : list[tuple[link:str, title:str]]
                    if Levenshtein.ratio(word, search) > 0.8:
                        feeds_list.append(feed.title)
                        break
        else:
            for feed in feeds:
                feeds_list.append(feed.title)
        self.value = feeds_list[self.get_choice(feeds_list)]
        self.cursor_position = len(self.value)


class TitledAutoCompletionBox(npyscreen.TitleFilename):
    '''Questa è la classe wrapper con testo dell'autocompletamento personalizzato.'''
    _entry_type = AutoCompletionBox
