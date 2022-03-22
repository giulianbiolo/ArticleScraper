'''Questo modulo implementa la classe della finestra di ricerca.'''
import npyscreen
from app.scrapers.base.Feed import Feed
from app.utils import load_article
from app.TitledAutoCompletionBox import TitledAutoCompletionBox


class BrowserBox(npyscreen.ActionForm):
    '''Questa classe gestisce il form di ricerca degli articoli.'''

    def create(self):
        '''Questo è il metodo di definizione/creazione di elementi grafici della pagina Browser.'''
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
        article_title: str = self.browsing_box.value
        try:
            feed: Feed = [feed for feed in self.find_parent_app().feeds if feed.title == article_title][0]
            article_link: str = feed.link
        except:
            article_link: str = ""
        if article_title == "":
            npyscreen.notify_confirm("Please enter a valid filename...")
            return
        if article_link == "":
            npyscreen.notify_confirm("Article not found...")
            return
        title, description, body = load_article(article_link)
        self.parentApp.getForm("ARTICLE").title_box.value = title
        self.parentApp.getForm("ARTICLE").description_box.value = description
        self.parentApp.getForm("ARTICLE").body_box.values = body.split("\n")
        self.parentApp.switchForm("ARTICLE")

    def on_quit(self, _):
        '''Questo metodo gestisce la chiusura dell'applicazione.'''
        self.parentApp.switchForm(None)
