'''Questo è il modulo principale per la gestione dell'interfaccia grafica all'interno del progetto.'''
import os
import pytermgui as ptg


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


class GUI:
    def __init__(self, filename: str, feeds: list[tuple[str, str]]) -> None:
        '''Questo è il costruttore della classe GUI.'''
        self.filename: str = filename
        self.feeds: list[tuple[str, str]] = feeds
        self.manager: ptg.WindowManager = ptg.WindowManager()
        self.title, self.description, self.body = load_article_file(filename)

    def _run_reload_pipeline(self) -> bool:
        '''Questo metodo esegue la pipeline del redraw della TUI.'''
        try:
            self._define_article_window()
            self._define_browser_window()
            self._define_v_split()
            self._define_layout()
        except Exception as e:
            print("Errore: ", e)
            return False
        return True

    def reload_article(self, filename: str) -> None:
        '''Questo metodo carica un nuovo articolo.'''
        self.manager.close(self.layout)
        self.filename = filename
        self.title, self.description, self.body = load_article_file(filename)
        res: bool = self._run_reload_pipeline()
        if res is False:
            print("Errore durante il caricamento dell'articolo...")
            return
        self.manager.add(self.layout)
        self.manager.alert("Articolo caricato!")

    def _define_article_window(self) -> None:
        '''Questo metodo definisce la finestra dell'articolo.'''
        self.article_window = ptg.Window(
            ptg.Label("[15 bold inverse]" + self.title),
            ptg.Label(),
            ptg.Label("[248 bold inverse]" + self.description),
            ptg.Label(),
            ptg.Label("[248]" + self.body),
        )
        self.article_window.allow_fullscreen = True
        self.article_window.overflow = ptg.Overflow.RESIZE

    def _define_browser_window(self) -> None:
        '''Questo metodo definisce la finestra del browser.'''
        self.article_buttons: list = []
        self.browser_window = ptg.Window(
            ptg.Label("[248 bold inverse]Feeds"),
            ptg.Label(),
        )
        self.browser_window._add_widget(ptg.Button("Articolo 1", lambda *_: self.reload_article("articolo.txt")))
        self.browser_window._add_widget(ptg.Label())
        for title, link in self.feeds:
            self.browser_window._add_widget(ptg.Button(str(title), lambda *_: self.reload_article(str(link))))
            self.browser_window._add_widget(ptg.Label())
        
        #self.browser_window.set_widgets(self.article_buttons)
        self.browser_window.allow_fullscreen = True
        self.browser_window.overflow = ptg.Overflow.RESIZE

    def _define_v_split(self) -> None:
        '''Questo metodo definisce il divisorio verticale della TUI.'''
        self.v_split = ptg.Splitter(
            self.article_window,
            self.browser_window,
        )

    def _define_layout(self) -> None:
        '''Questo metodo definisce il wrapper generale della TUI.'''
        self.layout = ptg.Window(self.v_split)
        self.layout.is_noresize = False
        self.layout.allow_fullscreen = True
        self.layout.overflow = ptg.Overflow.RESIZE

    def run(self) -> None:
        '''Questo metodo avvia l'interfaccia grafica.'''
        res: bool = self._run_reload_pipeline()
        if res is False:
            print("Errore durante il caricamento dell'articolo...")
            return
        self.manager.add(self.layout)
        self.manager.run()


def test():
    '''Questo metodo testa la classe GUI.'''
    from time import time as now
    start_time: float = now()
    gui = GUI(
        "articolo.txt",
        [
            ("Articolo 1", "articolo.txt"),
            ("Articolo 2", "articolo2.txt"),
            ("Articolo 3", "articolo3.txt"),
            ("Articolo 4", "articolo4.txt")
        ]
    )
    end_time: float = now()
    print(f"Tempo di esecuzione: {str(end_time - start_time)} secondi.")
    gui.run()
    del gui


if __name__ == "__main__":
    test()
