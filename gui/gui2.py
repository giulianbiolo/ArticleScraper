'''Questo è il modulo principale per la gestione dell'interfaccia grafica all'interno del progetto.'''
import os
from weakref import CallableProxyType
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


class GUI(npyscreen.NPSApp):
    def main(self):
        '''Questo metodo gestisce il main loop della GUI.'''
        self.window = npyscreen.FormMultiPageActionWithMenus(name="Welcome to GBJournal!")
        self.window.add(npyscreen.TitleFilename, name="Filename:", w_id="filename")
        self.window.add_handlers({
            # On Submit
            "^S": self.on_submit,
            # On File Browser
            "^D": self.on_browser_open,
        })
        title, description, body = "", "", ""
        self.window.add_page()
        self.window.add(npyscreen.FixedText, name="Title:", value=title, w_id="title")
        self.window.add(npyscreen.FixedText, name="Description:", value=description, w_id="description")
        self.window.add(npyscreen.FixedText, name="Body:", value=body, w_id="body")
        self.window.edit()

    def on_submit(self, _):
        '''Questo metodo gestisce la scelta di un articolo.'''
        filename: str = self.window.get_widget("filename").value
        if filename == "":
            npyscreen.notify_confirm("Please enter a valid filename...")
            return
        if not os.path.isfile(filename):
            npyscreen.notify_confirm("File not found...")
            return
        title, description, body = load_article_file(filename)
        self.window.get_widget("title").value = title
        self.window.get_widget("description").value = description
        self.window.get_widget("body").value = body
        self.window.switch_page(1)
        self.window.edit()

    def on_browser_open(self, _):
        '''Questo metodo gestisce l'apertura del browser di articoli'''
        self.window.get_widget("filename").value = ""
        self.window.switch_page(0)
        self.window.edit()



def test():
    '''Questo metodo testa la classe GUI.'''
    from time import time as now
    start_time: float = now()
    app = GUI()
    app.run()
    end_time: float = now()
    print(f"Tempo di esecuzione: {str(end_time - start_time)} secondi.")


if __name__ == "__main__":
    test()
