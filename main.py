'''Questo è il file principale del progetto. ArticleScraper raccoglie tutti gli articoli di giornale pubblicati nel mondo, e li salva in un database.'''
from threading import Thread
from modules.Feed import Feed
from modules.Ansa import Ansa
from modules.WallStreetJournal import WSJ
from gui import GUI


def main() -> None:
    '''Questo è il main del programma. Qui gestisco la logica di più alto livello.'''
    # Creo un processo per ogni notiziario da analizzare
    ansa: Ansa = Ansa()
    wsj: WSJ = WSJ()
    threads = []
    threads.append(Thread(target=ansa._load_feeds))
    threads.append(Thread(target=wsj._load_feeds))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    all_feeds: list[Feed] = []
    all_feeds.extend(ansa.fetch_all())
    all_feeds.extend(wsj.fetch_all())
    gui: GUI = GUI(all_feeds)
    gui.run()
    return


if __name__ == '__main__':
    main()
