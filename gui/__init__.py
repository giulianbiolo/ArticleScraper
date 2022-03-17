'''Questo è il modulo principale per la gestione dell'interfaccia grafica all'interno del progetto.'''
import npyscreen
from modules.Feed import Feed
from gui.BrowserBox import BrowserBox
from gui.ArticleBox import ArticleBox


npyscreen.NPSAppManaged.STARTING_FORM = "BROWSER"


class GUI(npyscreen.NPSAppManaged):
    '''Questa classe permette di gestire la GUI.'''

    def __init__(self, feeds: list[Feed], *args, **kwargs):
        '''Questo metodo viene chiamato all'avvio dell'applicazione.'''
        super().__init__(*args, **kwargs)
        self.feeds: list[Feed] = feeds

    def onStart(self):
        '''Questo metodo viene chiamato all'avvio dell'applicazione.'''
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("BROWSER", BrowserBox, name="Welcome To GBJournal!")
        self.addForm("ARTICLE", ArticleBox, name="Welcome To GBJournal!")
