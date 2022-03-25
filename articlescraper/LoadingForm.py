'''
This module implements the class LoadingForm,
which takes care of the graphical visualization of the loading page.
'''
from time import sleep
from threading import Thread
import npyscreen


class LoadingForm(npyscreen.ActionForm):
    '''This class implements the LoadingForm.'''

    def create(self):
        '''This method defines the basic graphical elements of the page.'''
        self.loading_text = self.add(
            npyscreen.TitleText, name="Loading...", w_id="loading")
        self.loading_text.set_relyx(
            self.useable_space()[0] // 2, self.useable_space()[1] // 2 - 5)
        self.loading_text.max_height = 3
        self.add_handlers({
            "^X": self.on_quit,
            "^C": self.on_quit,
        })
        self.listener = Thread(target=self.listen)
        self.listener.start()

    def listen(self):
        '''This method keeps on checking wheter self.feeds gets populated.'''
        feed_is_empty: bool = True
        while feed_is_empty:
            sleep(0.1)
            with self.find_parent_app().mutex:
                feed_is_empty = self.find_parent_app().feeds is None
        self.loading_text.value = "Loading complete!"
        self.loading_text.set_relyx(
            self.useable_space()[0] // 2, self.useable_space()[1] // 2 - 8)
        self.find_parent_app().switchForm("BROWSER")
        self.display()

    def on_quit(self, _) -> None:
        '''This method handles the quit functionality.'''
        self.find_parent_app().switchForm(None)
