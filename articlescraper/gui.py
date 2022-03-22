'''Questo è il modulo principale di gestione dell'interfaccia grafica all'interno del progetto.'''
from time import sleep as wait
from threading import Thread, Lock
from weakref import CallableProxyType
import npyscreen
from articlescraper.scrapers.base.Feed import Feed
from articlescraper.scrapers.Ansa import Ansa
from articlescraper.scrapers.WallStreetJournal import WSJ
from articlescraper.BrowserBox import BrowserBox
from articlescraper.ArticleBox import ArticleBox
from articlescraper.LoadingForm import LoadingForm


npyscreen.NPSAppManaged.STARTING_FORM = "LOADING"


class GUI(npyscreen.NPSAppManaged):
    '''Questa classe permette di gestire la GUI.'''

    def __init__(self, *args, **kwargs):
        '''Questo metodo viene chiamato all'avvio dell'applicazione.'''
        super().__init__(*args, **kwargs)
        self.feeds: list[Feed] = None
        self.loading: CallableProxyType[LoadingForm] = None
        self.browser: CallableProxyType[BrowserBox] = None
        self.article: CallableProxyType[ArticleBox] = None
        self.mutex: Lock = Lock()

    def onStart(self):
        '''Questo metodo viene chiamato all'avvio dell'applicazione.'''
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.loading = self.addForm("LOADING", LoadingForm, name="Loading...")
        self.browser = self.addForm(
            "BROWSER", BrowserBox, name="Welcome To GBJournal!")
        self.article = self.addForm(
            "ARTICLE", ArticleBox, name="Welcome To GBJournal!")
        Thread(target=self.load_data).start()

    def load_data(self) -> list[Feed]:
        '''
        Questo metodo carica i dati forniti dai vari scraper.
        Per aggiungere uno scraper bisogna solo instanziarlo nella lista 'modules'.
        '''
        threads: list[Thread] = []
        # modules: list = [ ..., YourAwesomeScraper(self.mutex)]
        modules: list = [Ansa(self.mutex), WSJ(self.mutex)]
        for module in modules:
            threads.append(
                Thread(target=module.load_feeds, args=(self.mutex,)))
        for thread in threads:
            thread.start()
        all_loaded: bool = False
        while not all_loaded:
            wait(0.1)
            with self.mutex:
                all_loaded = True
                for module in modules:
                    all_loaded = module.loaded
        all_feeds: list[Feed] = []
        for module in modules:
            all_feeds.extend(module.fetch_all())
        with self.mutex:
            self.feeds = all_feeds
