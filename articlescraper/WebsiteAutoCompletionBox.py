'''
This module implements the class WebsiteAutoCompletionBox,
which takes care of the visualization of the scraper autocompletion box.
'''
import npyscreen


class AutoCompletionBox(npyscreen.Autocomplete):
    '''This class implements an autocompletion box.'''

    def auto_complete(self, _):
        '''This method handles the autocompletion of scrapers functionality.'''
        modules: list[str] = ["All", "Ansa", "WallStreetJournal", "NewYorkTimes"]
        search: str = self.value.strip().lower()
        if search != "":
            modules = [module for module in modules if module.strip().lower().startswith(search)]
        if len(modules) == 0:
            self.value = ""
            self.cursor_position = 0
            return
        if len(modules) == 1:
            self.value = modules[0]
            self.cursor_position = len(self.value)
            return
        self.value = modules[self.get_choice(modules)]
        self.cursor_position = len(self.value)


class WebsiteAutoCompletionBox(npyscreen.TitleFilename):
    '''This is a wrapper class for the personalized autocompletion box.'''
    _entry_type = AutoCompletionBox
