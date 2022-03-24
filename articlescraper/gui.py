'''
This is the main GUI module of the program.
It takes care of the graphical interface of the program.
'''
from time import sleep as wait
from threading import Thread, Lock
from weakref import CallableProxyType
from requests import Session as ReqSession
import npyscreen
from articlescraper.scrapers.base.Feed import Feed
from articlescraper.scrapers.Ansa import Ansa
from articlescraper.scrapers.WallStreetJournal import WSJ
from articlescraper.BrowserBox import BrowserBox
from articlescraper.ArticleBox import ArticleBox
from articlescraper.LoadingForm import LoadingForm


npyscreen.NPSAppManaged.STARTING_FORM = "LOADING"


class GUI(npyscreen.NPSAppManaged):
    '''This class implements the GUI of the program.'''

    def __init__(self, *args, **kwargs):
        '''
        This method gets called at the beginning of the program.
        Here we define some of the most fundamental variables of the program.
        '''
        super().__init__(*args, **kwargs)
        self.feeds: list[Feed] = None
        self.loading: CallableProxyType[LoadingForm] = None
        self.browser: CallableProxyType[BrowserBox] = None
        self.article: CallableProxyType[ArticleBox] = None
        self.mutex: Lock = Lock()
        self.session: ReqSession = ReqSession()

    def onStart(self):
        '''
        This method gets called at the beginning of the program.
        Here we define the various pages of the GUI.
        '''
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.loading = self.addForm("LOADING", LoadingForm, name="Loading...")
        self.browser = self.addForm(
            "BROWSER", BrowserBox, name="Welcome To GBJournal!")
        self.article = self.addForm(
            "ARTICLE", ArticleBox, name="Welcome To GBJournal!")
        Thread(target=self.load_data).start()

    def load_data(self) -> list[Feed]:
        '''
        This method loads the data given by the various scrapers.
        To add a new scraper, simply add it to the list 'modules' below.
        '''
        threads: list[Thread] = []
        # modules: list = [ ..., YourAwesomeScraper(self.mutex)]
        modules: list = [Ansa(self.mutex, self.session), WSJ(self.mutex, self.session)]
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
