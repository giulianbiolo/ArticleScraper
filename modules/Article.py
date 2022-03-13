'''Questo modulo contiene la classe Article.'''


class Article:
    def __init__(self, title="", description="", content="", author="", date="", link="") -> None:
        '''Questo è il costruttore della classe.'''
        self.title: str = title
        self.description: str = description
        self.link: str = link
        self.content: str = content
        self.date: str = date
        self.author: str = author

    def __str__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str(self.title)

    def __repr__(self) -> str:
        '''Questo metodo ritorna una stringa che rappresenta l'oggetto.'''
        return str(self.title)

    def __eq__(self, other) -> bool:
        '''Questo metodo ritorna True se due oggetti sono uguali.'''
        return self.title == other.title

    def __hash__(self) -> int:
        '''Questo metodo ritorna un hash per l'oggetto.'''
        return hash(self.title)

    def print(self) -> None:
        '''Questo metodo stampa l'oggetto.'''
        print("------------")
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Link: {self.link}")
        print(f"Content: {self.content}")
        print(f"Date: {self.date}")
        print(f"Author: {self.author}")
        print("------------")
