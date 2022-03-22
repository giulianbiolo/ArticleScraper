'''Questo modulo implementa la classe Feed.'''


class Feed:
    '''Questa è la classe che rappresenta il singolo feed rss.'''

    def __init__(self, link: str = "", title: str = "", lang: str = "it") -> None:
        '''Questo è il costruttore della classe.'''
        if link == "" or title == "":
            raise ValueError("Il feed deve avere sia un link che un titolo!")
        self.link: str = link
        self.title: str = title
        self.lang: str = lang

    def __str__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str(self.title)

    def __repr__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str(self.title)

    def __eq__(self, other) -> bool:
        '''Questo metodo ritorna True se due oggetti sono uguali.'''
        return self.title == other.title
