import npyscreen


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
