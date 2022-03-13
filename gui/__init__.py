'''Questo è il modulo principale per la gestione dell'interfaccia grafica all'interno del progetto.'''
import os
# from pygments.lexers.python import PythonLexer
# from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import LayoutDimension
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
import Levenshtein



# Dichiaro globali i KeyBindings e la Style per la GUI
bindings: KeyBindings = KeyBindings()
style_dict: dict[str, str] = {
    "status": "reverse",                  # Imposto il colore della status su 'reverse'
    "status.position": "#aaaa00",         # Colore posizione cursore in statusbar
    "status.key": "#ffaa00",              # Colore keybindings in statusbar
    "searching": "reverse",               # Colore per la barra di ricerca in ricerca
    "not-searching": "#888888",           # Colore per la barra di ricerca in idle
    "title": "reverse",                   # Imposto il colore del titolo su 'reverse'
    "title-background": "#228822",        # Sfondo verde
    "description": "reverse",             # Imposto colore descrizione su 'reverse'
    "description-background": "#dddddd",  # Sfondo grigio
    "body": "#666666",                    # Colore del testo
    "body-background": "#666666",         # Sfondo del testo
    "browser": "#888888",                 # Colore del browser
    "browser-background": "#888888",      # Sfondo del browser
}


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


def get_opened_page_application(title: str, description: str, body: str):
    '''Questo metodo carica un articolo e costruisce il layout della pagina da renderizzare.'''
    search_field = SearchToolbar(
        text_if_not_searching=[
            ("class:not-searching", "Press '/' to start searching.")],
        ignore_case=True,
        forward_search_prompt=[("class:searching", ">:")],
        backward_search_prompt=[("class:searching", "<:")],
    )
    text_area = TextArea(
        text=body,
        read_only=True,
        scrollbar=True,
        line_numbers=True,
        search_field=search_field,
        # lexer=PygmentsLexer(PythonLexer), # Per l'highlighting di codice
    )
    page_container = HSplit([
        # The top toolbar.
        Window(
            content=FormattedTextControl(
                get_statusbar_text("< Articolo >", text_area)),
            height=LayoutDimension.exact(2),
            align=WindowAlign.RIGHT,
            style="class:status",
        ),
        # The title of the file.
        Window(
            content=FormattedTextControl(
                [("class:title", title)]),
            height=LayoutDimension.exact(2),
            align=WindowAlign.CENTER,
            style="class:title-background",
        ),
        # The description of the file.
        Window(
            content=FormattedTextControl(
                [("class:description", description)]),
            height=LayoutDimension.exact(
                description.count("\n") + 2),
            align=WindowAlign.CENTER,
            style="class:description-background",
        ),
        # The body of the file.
        text_area,
        # The bottom toolbar.
        search_field,
    ])
    root_container = VSplit([
        page_container,
        Window(width=1, char='|'),
        Window(
            content=FormattedTextControl([("class:browser", '1) A\n2) B\n3) C')]),
            align=WindowAlign.LEFT,
            style="class:browser-background",
        ),
    ])
    style = Style.from_dict(style_dict)
    application = Application(
        layout=Layout(root_container),
        key_bindings=bindings,
        enable_page_navigation_bindings=True,
        mouse_support=True,
        style=style,
        full_screen=True,
    )
    return search_field, text_area, root_container, style, application


def get_statusbar_text(title, text_area) -> list[tuple[str, str]]:
    '''Questo metodo ritorna il testo che verrà visualizzato nella barra di stato.'''
    return [
        ("class:status", title + " - "),
        (
            "class:status.position",
            "{}:{}".format(
                text_area.document.cursor_position_row + 1,
                text_area.document.cursor_position_col + 1,
            ),
        ),
        ("class:status", " - Press "),
        ("class:status.key", "'CTRL+C'"),
        ("class:status", " or "),
        ("class:status.key", "':q'"),
        ("class:status", " to exit, "),
        ("class:status.key", "/"),
        ("class:status", " for searching."),
    ]


class GUI:
    def __init__(self, filename: str) -> None:
        '''Questo è il costruttore della classe GUI.'''
        self.filename: str = filename
        self.title, self.description, self.body = load_article(filename)
        self.search_field, self.text_area, self.root_container, self.style, self.application = get_opened_page_application(
            self.title, self.description, self.body)

    def run(self) -> None:
        '''Questo metodo avvia l'interfaccia grafica.'''
        self.application.run()
        # self.application._redraw(render_as_done=True)


@bindings.add("c-c")
@bindings.add(":", "q")
def exit_editor(event):
    '''Questo metodo termina il programma.'''
    event.app.exit()

@bindings.add("c-i")
def open_file_browser(event):
    '''Questo metodo apre il menu di ricerca file.'''
    query: str = input(">: ")
    if query == "":
        return
    files: list[str] = os.listdir(os.getcwd())
    files = [f for f in files if f.endswith(".txt")]
    files = [f for f in files if Levenshtein.ratio(f.lower(), query.lower()) > 0.7]
    if len(files) == 0:
        print("No files found.")
        return
    for i, f in enumerate(files):
        print(f"{str(i+1)}) {f}")
    choice: int = int(input(">: "))
    if choice == 0:
        return
    GUI(files[choice-1]).run()


@bindings.add("c-h")
def open_file(event):
    '''Questo metodo apre un file.'''
    #filename: str = event.app.layout.container.children[0].content.text
    filename: str = "articolo2.txt"
    title, description, body = load_article(filename)
    search_field, text_area, root_container, style, application = get_opened_page_application(
        title, description, body)
    event.app.layout.container = root_container


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
