'''This module contains the Article class.'''


class Article:
    '''This class represents an Article.'''

    def __init__(self, title="", description="", content="", author="", date="", link="") -> None:
        '''This is the constructor of the class.'''
        self.title: str = title
        self.description: str = description
        self.link: str = link
        self.content: str = content
        self.date: str = date
        self.author: str = author

    def __eq__(self, other) -> bool:
        '''This method returns True if the objects are equal.'''
        return self.title == other.title

    def print(self) -> None:
        '''This method prints the object.'''
        print("------------")
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Link: {self.link}")
        print(f"Content: {self.content}")
        print(f"Date: {self.date}")
        print(f"Author: {self.author}")
        print("------------")
