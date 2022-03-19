'''Questo è il file principale del progetto. ArticleScraper raccoglie tutti gli articoli di giornale pubblicati nel mondo, e li salva in un database.'''
from gui import GUI


def main() -> None:
    '''Questo è il main del programma. Qui gestisco la logica di più alto livello.'''
    gui: GUI = GUI()
    gui.run()


if __name__ == '__main__':
    main()
