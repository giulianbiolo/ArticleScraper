# ArticleScraper

ArticleScraper is a simple web scraper that scrapes articles from every newspaper website and lets you read them from the command line.

## Installation

### Windows
-----------

You can just download the prepackaged binary from [here](https://github.com/giulianbiolo/ArticleScraper/releases) and run it.  

However if you prefer to bundle it yourself from source, follow the guide below.

### Linux / Mac OS X
--------------------

The fastest and easiest way is to download the source code.  
Remember to install all the required dependencies by running:  
```
pip install -r requirements.txt
```

And then you can just execute the app.py file:  
```
python app.py
```

However if you really want a bundled version, you can package it yourself by following the guide below, starting at point 2.

## Bundling From Source
-----------------------

1. Download the source code.
2. Install all the required dependencies by running:
    ```
    pip install -r requirements.txt
    ```
3. Run the app.py file:
    ```
    python app.py
    ```
4. To package the app, you first need to install the `pyinstaller` package like this:  
    ```
    pip install pyinstaller
    ```
5. Now run the following command to package the app:
    ```
    pyinstaller --onefile app.py
    ```
6. The app will be packaged in the `dist` folder.

## Contributing Changes
-----------------------

ArticleScraper is meant to be very flexible and easy to modify and extend.  

Every website is modularized and you can add your own by creating a new file in the `scrapers` folder.  

You'll have to create a class of the name of the file that inherits from the `WebScraper` class and implements the `load_article` method and overrides the `load_feeds` method by passing the rss-feeds `urls` as a list of strings.  
Also you'll have to implement a `is_<your-module>_article` method that returns a boolean value indicating if the article is of the type you're trying to scrape.

To get a better understanding you should read the code of `Ansa` or `WallStreetJournal` scrapers.  
They are both very basic examples of how to create a new scraper, and hopefully they're intuitive enough to understand.  

Having done so all you have to do is to add the new scraper to the `gui.py` file, inside the `modules` list.  
As of today you have to add your module to `utils.py` too, by adding the lines:  
```
elif is_<your-module>_article(link):
    from articlescraper.scrapers.<your-module>
    import load_article as <your-module>_load_article
    article = <your-module>_load_article(link)
```
If you want the scraper-selection feature to work you have to add your scraper name inside the `modules` list in the `WebsiteAutoCompletionBox.py` file.


After doing all of this you should be able to run the app and read your new scraped articles.  
At this point, if everything works fine, you can open a pull request to add your module to the repository.  
Otherwise you might open an issue to discuss with me what's failing.  
