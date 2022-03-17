'''Questo è il file principale del progetto. ArticleScraper raccoglie tutti gli articoli di giornale pubblicati nel mondo, e li salva in un database.'''
from modules.Ansa import Ansa
from modules.WallStreetJournal import WSJ
from modules.Article import Article
from modules.Feed import Feed
from gui import GUI


def main() -> None:
    '''Questo è il main del programma. Qui gestisco la logica di più alto livello.'''
    ansa: Ansa = Ansa()
    # Ritorna una lista di titoli di articoli attinenti
    #feeds: list[tuple] = ansa.find_from_title("Ucraina")
    #print("Titoli Trovati: " + str(len(feeds)))
    #for link, title in feeds:
    #    print("------")
    #    print(link)
    #    print(title)
    #    print("------")
    #article: Article = ansa.load_article(feeds[0][0])  # Carica un articolo
    #article.print()  # Stampa l'articolo

    wsj: WSJ = WSJ()
    # Ritorna una lista di titoli di articoli attinenti
    #feeds: list[tuple] = wsj.find_from_title("Ukraine")
    #print("Titoli Trovati: " + str(len(feeds)))
    #for link, title in feeds:
    #    print("------")
    #    print(link)
    #    print(title)
    #    print("------")
    #article: Article = wsj.load_article(feeds[0][0])  # Carica un articolo
    #article.print()  # Stampa l'articolo

    all_feeds: list[Feed] = []
    all_feeds.extend(ansa.find_all())
    #all_feeds.extend(wsj.find_all())
    gui: GUI = GUI(all_feeds)
    gui.run()
    return


if __name__ == '__main__':
    main()
