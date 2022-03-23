'''
This is the main file of the program.  
ArticleScraper gathers newspapers and articles from the web 
and lets you read them from the command line.
'''

from articlescraper import GUI


def main() -> None:
    '''This is the main function of the program. Here the GUI is initialized.'''
    gui: GUI = GUI()
    gui.run()


if __name__ == '__main__':
    main()
