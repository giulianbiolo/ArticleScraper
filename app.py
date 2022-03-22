'''
Questo è il file principale del progetto.
ArticleScraper raccoglie articoli di giornale da tutto il mondo
e ti permette di visualizzarli comodamente dal tuo terminale.
'''
#from app import GUI
from articlescraper import GUI


def main() -> None:
    '''Questo è il main del programma. Qui gestisco la logica di più alto livello.'''
    gui: GUI = GUI()
    gui.run()


if __name__ == '__main__':
    main()
