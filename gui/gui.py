'''Questo è il modulo principale per la gestione dell'interfaccia grafica all'interno del progetto.'''
import os
import npyscreen
import curses


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


def prettify_text(text: str) -> str:
    '''Questo metodo permette di formattare il testo della GUI.'''
    return text.replace("  ", "\n").replace("   ", "\n").replace("    ", "\n").replace(". ", ".\n")


npyscreen.NPSAppManaged.STARTING_FORM = "BROWSER"


class GUI(npyscreen.NPSAppManaged):
    '''Questa classe permette di gestire la GUI.'''

    def onStart(self):
        '''Questo metodo viene chiamato all'avvio dell'applicazione.'''
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        self.addForm("BROWSER", BrowserBox, name="Welcome To GBJournal!")
        self.addForm("ARTICLE", ArticleBox, name="Welcome To GBJournal!")


class BrowserBox(npyscreen.ActionForm):
    '''Questa classe gestisce il form di ricerca degli articoli.'''

    def create(self):
        '''Questo è il metodo di definizione e creazione degli elementi grafici della pagina Browser.'''
        #self.browsing_box = self.add(
        #    npyscreen.TitleFilename, name="Filename:", w_id="filename")
        self.browsing_box = self.add(
            TitledAutoCompletionBox, name="Filename: ", w_id="filename")
        self.browsing_btn = self.add(
            npyscreen.ButtonPress, name="Browse", w_id="browse")
        self.browsing_box.set_relyx(self.browsing_box.rely + 1, self.browsing_box.relx + 4)
        self.browsing_btn.set_relyx(self.browsing_btn.rely + 2, self.browsing_btn.relx + 4)
        self.browsing_btn.whenPressed = self.on_ok

    def on_ok(self):
        '''Questo metodo viene chiamato quando viene premuto il pulsante OK / Browse.'''
        filename: str = self.browsing_box.value
        if filename == "":
            npyscreen.notify_confirm("Please enter a valid filename...")
            return
        if not os.path.isfile(filename):
            npyscreen.notify_confirm("File not found...")
            return
        title, description, body = load_article_file(filename)
        self.parentApp.getForm("ARTICLE").title_box.value = title
        self.parentApp.getForm("ARTICLE").description_box.value = description
        self.parentApp.getForm("ARTICLE").body_box.values = body.split("\n")
        self.parentApp.switchForm("ARTICLE")


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
        self.description_box.set_relyx(self.description_box.rely + 1, self.description_box.relx + 10)
        self.description_box.max_height = 5
        self.body_box.set_relyx(self.body_box.rely + 2, self.body_box.relx + 2)
        self.add_handlers({
            "^B": self.on_back,
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
        # expand ~
        self.value = os.path.expanduser(self.value)

        for i in range(1):
            dir, fname = os.path.split(self.value)
            # Let's have absolute paths.
            dir = os.path.abspath(dir)
    
            if self.value == '':
                self.value=dir
                break
    
            try: 
                flist = os.listdir(dir)
            except:
                self.show_brief_message("Can't read directory!")
                break

            flist = [os.path.join(dir, x) for x in flist]
            possibilities = list(filter(
                (lambda x: os.path.split(x)[1].startswith(fname)), flist
                ))
            # Le Possibilities sono i /path/vari/.../[Possibility[i]]

            if len(possibilities) is 0:
                # can't complete
                curses.beep()
                break

            if len(possibilities) is 1:
                if self.value != possibilities[0]:
                    self.value = possibilities[0]
                if os.path.isdir(self.value) \
                    and not self.value.endswith(os.sep):
                    self.value = self.value + os.sep
                else:
                    if not os.path.isdir(self.value):
                        self.h_exit_down(None)
                    break

            if len(possibilities) > 1:
                filelist = possibilities
            else:
                filelist = flist #os.listdir(os.path.dirname(self.value))
    
            filelist = list(map((lambda x: os.path.normpath(os.path.join(self.value, x))), filelist))
            files_only = []
            dirs_only = []

            if fname.startswith('.'):
                filelist = list(filter((lambda x: os.path.basename(x).startswith('.')), filelist))
            else:
                filelist = list(filter((lambda x: not os.path.basename(x).startswith('.')), filelist))

            for index1 in range(len(filelist)):
                if os.path.isdir(filelist[index1]) and not filelist[index1].endswith(os.sep):
                    filelist[index1] = filelist[index1] + os.sep

                if os.path.isdir(filelist[index1]):
                    dirs_only.append(filelist[index1])
            
                else:
                    files_only.append(filelist[index1])
    
            dirs_only.sort()
            files_only.sort()
            combined_list = dirs_only + files_only
            combined_list.insert(0, self.value)
            self.value = combined_list[self.get_choice(combined_list)]
            break
        os.path.normcase(self.value)
        self.cursor_position=len(self.value)


class TitledAutoCompletionBox(npyscreen.TitleFilename):
    '''Questa è la classe wrapper con testo dell'autocompletamento personalizzato.'''
    _entry_type = AutoCompletionBox


def test():
    '''Questo metodo testa la classe GUI.'''
    GUI().run()


if __name__ == "__main__":
    test()
