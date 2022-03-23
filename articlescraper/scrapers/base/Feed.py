'''This method implements the Feed class.'''


class Feed:
    '''This class represents a single RSS Feed.'''

    def __init__(self, link: str = "", title: str = "", lang: str = "it", scraper: str = "") -> None:
        '''This is the constructor of the class.'''
        if link == "" or title == "":
            raise ValueError("Il feed deve avere sia un link che un titolo!")
        self.link: str = link
        self.title: str = title
        self.lang: str = lang
        self.scraper: str = scraper

    def __str__(self) -> str:
        '''This method returns a string that represents the object.'''
        return str(self.title)

    def __repr__(self) -> str:
        '''This method returns a string that represents the object.'''
        return str(self.title)

    def __eq__(self, other) -> bool:
        '''This method returns True if the objects are equal.'''
        return self.title == other.title
