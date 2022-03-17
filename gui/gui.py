'''Questo è il modulo principale per la gestione dell'interfaccia grafica all'interno del progetto.'''
import logging
import npyscreen
from modules.Article import Article
from modules.Ansa import is_ansa_article
from modules.WallStreetJournal import is_wsj_article

logger = None


def load_article_file(filename: str) -> tuple[str, str, str]:
    '''Questo metodo carica un articolo da un file.'''
    title: str = ""
    description: str = ""
    body: str = ""
    with open(filename, "rb") as file:
        raw_data: str = file.read().decode("utf-8")
        title = raw_data.split("\n")[0].strip()
        description = raw_data.split("\n")[1].strip()
        body = "\n".join(raw_data.split("\n")[2:]).strip()
    return title, description, prettify_text(body)


def load_article(link: str) -> tuple[str, str, str]:
    '''Questo metodo carica un articolo dal link.'''
    title: str = ""
    description: str = ""
    body: str = ""
    if is_ansa_article(link):
        from modules.Ansa import Ansa
        ansa: Ansa = Ansa()
        article: Article = ansa.load_article(link)
        title = article.title
        description = article.description
        body = prettify_text(article.content)
    elif is_wsj_article(link):
        from modules.WallStreetJournal import WSJ
        wsj: WSJ = WSJ()
        article: Article = wsj.load_article(link)
        title = article.title
        description = article.description
        body = prettify_text(article.content)
    else:
        logger.error("Link non valido: " + link)
    return title, description, body


def prettify_text(text: str) -> str:
    '''Questo metodo permette di formattare il testo della GUI.'''
    return text.replace("  ", "\n").replace("   ", "\n").replace("    ", "\n").replace(". ", ".\n")


npyscreen.NPSAppManaged.STARTING_FORM = "BROWSER"


class GUI(npyscreen.NPSAppManaged):
    '''Questa classe permette di gestire la GUI.'''

    def __init__(self, feeds: list[tuple], *args, **kwargs):
        '''Questo metodo viene chiamato all'avvio dell'applicazione.'''
        super().__init__(*args, **kwargs)
        self.feeds = feeds

    def onStart(self):
        '''Questo metodo viene chiamato all'avvio dell'applicazione.'''
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("BROWSER", BrowserBox, name="Welcome To GBJournal!")
        self.addForm("ARTICLE", ArticleBox, name="Welcome To GBJournal!")


class BrowserBox(npyscreen.ActionForm):
    '''Questa classe gestisce il form di ricerca degli articoli.'''

    def create(self):
        '''Questo è il metodo di definizione e creazione degli elementi grafici della pagina Browser.'''
        self.browsing_box = self.add(
            TitledAutoCompletionBox, name="Filename: ", w_id="filename")
        self.browsing_btn = self.add(
            npyscreen.ButtonPress, name="Browse", w_id="browse")
        self.browsing_box.set_relyx(
            self.browsing_box.rely + 1, self.browsing_box.relx + 4)
        self.browsing_btn.set_relyx(
            self.browsing_btn.rely + 2, self.browsing_btn.relx + 4)
        self.browsing_btn.whenPressed = self.on_ok
        self.add_handlers({
            "^X": self.on_quit,
        })

    def on_ok(self):
        '''Questo metodo viene chiamato quando viene premuto il pulsante OK / Browse.'''
        article_link: str = self.browsing_box.value
        if article_link == "":
            npyscreen.notify_confirm("Please enter a valid filename...")
            return
        if article_link not in [link for link, _ in self.find_parent_app().feeds]:
            npyscreen.notify_confirm("File not found...")
            return
        title, description, body = load_article(article_link)
        self.parentApp.getForm("ARTICLE").title_box.value = title
        self.parentApp.getForm("ARTICLE").description_box.value = description
        self.parentApp.getForm("ARTICLE").body_box.values = body.split("\n")
        self.parentApp.switchForm("ARTICLE")

    def on_quit(self, _):
        '''Questo metodo gestisce la chiusura dell'applicazione.'''
        self.parentApp.switchForm(None)


class ArticleBox(npyscreen.ActionForm):
    '''Questa classe gestisce il form di visualizzazione articoli.'''

    def create(self):
        '''Questo è il metodo di definizione e creazione degli elementi grafici della pagina Article.'''
        self.title_box = self.add(
            npyscreen.TitleFixedText, name="Title:", w_id="title")
        self.description_box = self.add(
            npyscreen.TitleFixedText, name="Description:", w_id="description")
        self.body_box = self.add(npyscreen.Pager, name="Body:", w_id="body")
        self.title_box.set_relyx(self.title_box.rely, self.title_box.relx + 10)
        self.title_box.max_height = 3
        self.description_box.set_relyx(
            self.description_box.rely + 1, self.description_box.relx + 10)
        self.description_box.max_height = 5
        self.body_box.set_relyx(self.body_box.rely + 2, self.body_box.relx + 2)
        self.add_handlers({
            "^B": self.on_back,
            "^X": self.on_quit,
        })

    def on_ok(self):
        '''Questo metodo gestisce la funzionalità del tasto OK.'''
        self.on_back(None)

    def on_back(self, _):
        '''Questo metodo riporta al browser file.'''
        self.parentApp.getForm("BROWSER").browsing_box.value = ""
        self.parentApp.switchForm("BROWSER")

    def on_quit(self, _):
        '''Questo metodo gestisce la chiusura dell'applicazione.'''
        self.parentApp.switchForm(None)


class AutoCompletionBox(npyscreen.Autocomplete):
    '''Questa classe gestisce il funzionamento dell'autocompletamento degli articoli.'''

    def auto_complete(self, _):
        '''Questo è l'override del metodo che gestisce i feed degli autocompletamenti.'''
        feeds_list = []
        feeds = self.find_parent_app().feeds
        for _, title in feeds:
            feeds_list.append(title)
        self.value = feeds_list[self.get_choice(feeds_list)]
        for link, title in feeds:
            if title == self.value:
                self.value = link
        self.cursor_position = len(self.value)


class TitledAutoCompletionBox(npyscreen.TitleFilename):
    '''Questa è la classe wrapper con testo dell'autocompletamento personalizzato.'''
    _entry_type = AutoCompletionBox


def test():
    '''Questo metodo testa la classe GUI.'''
    global logger
    FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT, filename="log.txt",
                        level=logging.DEBUG, filemode='w')
    logger = logging.getLogger('mylogger')
    handler = logging.FileHandler('mylog.log')
    logger.addHandler(handler)
    GUI([
        ('link_1', 'Articolo 1'),
        ('link_2', 'Articolo 2'),
        ('link_3', 'Articolo 3'),
        ('link_4', 'Articolo 4'),
        ('link_5', 'Articolo 5'),
        ('link_6', 'Articolo 6'),
        ('link_7', 'Articolo 7'),
        ('link_8', 'Articolo 8'),
        ('link_9', 'Articolo 9'),
        ('link_10', 'Articolo 10'),
    ]).run()


if __name__ == "__main__":
    test()
