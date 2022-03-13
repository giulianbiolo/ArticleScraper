'''Questo è il modulo principale per la gestione dell'interfaccia grafica all'interno del progetto.'''
import os
import pytermgui as ptg
import Levenshtein


def load_article(filename: str) -> tuple[str, str, str]:
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
    def __init__(self, filename: str) -> None:
        '''Questo è il costruttore della classe GUI.'''
        self.filename: str = filename
        self.title, self.description, self.body = load_article(filename)

    def run(self) -> None:
        '''Questo metodo avvia l'interfaccia grafica.'''
        with ptg.WindowManager() as manager:
            '''
            demo = ptg.Window(
                ptg.Label("[210 bold]Benvenuto su GBJournal!"),
                ptg.Label(),
                ptg.InputField(prompt="Cerca: "),
                ptg.Label(),
                ptg.Button("Submit!", lambda *_: manager.alert("Form submitted!")),
            )
            '''
            article_window = ptg.Window(
                ptg.Label("[15 bold inverse]" + self.title),
                ptg.Label(),
                ptg.Label("[248 bold inverse]" + self.description),
                ptg.Label(),
                ptg.Label("[248]" + self.body),
            )
            article_window.allow_fullscreen = True
            article_window.overflow = ptg.Overflow.RESIZE
            browser_window = ptg.Window(
                ptg.InputField(prompt="Cerca: "),
                ptg.Label(),
                ptg.Button("Submit!", lambda *_: manager.alert("Form submitted!")),
            )
            browser_window.allow_fullscreen = True
            browser_window.overflow = ptg.Overflow.RESIZE
            v_split = ptg.Splitter(
                article_window,
                browser_window,
            ),
            layout = ptg.Window(
                v_split,
            )
            layout.is_noresize = False
            layout.allow_fullscreen = True
            layout.overflow = ptg.Overflow.RESIZE
            

            manager.add(layout)
            manager.run()


def test():
    '''Questo metodo testa la classe GUI.'''
    from time import time as now
    start_time: float = now()
    gui = GUI("articolo.txt")
    end_time: float = now()
    print(f"Tempo di esecuzione: {str(end_time - start_time)} secondi.")
    gui.run()
    del gui


if __name__ == "__main__":
    test()
