'''
This module implements the class ArticleBox,
which takes care of the graphical visualization of the articles.
'''

import npyscreen


class ArticleBox(npyscreen.ActionForm):
    '''This class implements the ArticleBox.'''

    def create(self):
        '''This method defines the basic graphical elements of the page.'''
        self.title_box = self.add(
            npyscreen.TitleFixedText, name="Title:", w_id="title")
        self.description_box = self.add(
            npyscreen.TitleFixedText, name="Description:", w_id="description")
        self.body_box = self.add(npyscreen.Pager, name="Body:", w_id="body")
        self.title_box.set_relyx(self.title_box.rely, self.title_box.relx)
        self.title_box.max_height = 3
        self.description_box.set_relyx(
            self.description_box.rely + 1, self.description_box.relx)
        self.description_box.max_height = 5
        self.body_box.set_relyx(self.body_box.rely + 2, self.body_box.relx + 2)
        self.title_box.use_two_lines = True
        self.body_box.autowrap = True
        self.add_handlers({
            "^B": self.on_back,
            "q": self.on_back,
            "^X": self.on_quit,
        })

    def on_ok(self):
        '''This method handles the OK button.'''
        self.on_back(None)

    def on_back(self, _):
        '''This method handles the "go back" functionality.'''
        self.parentApp.getForm("BROWSER").browsing_box.value = ""
        self.parentApp.switchForm("BROWSER")

    def on_quit(self, _):
        '''This method handles the quit functionality.'''
        self.parentApp.switchForm(None)
