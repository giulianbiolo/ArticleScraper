'''Questo modulo implementa la classe della finestra di caricamento.'''
from time import sleep
from threading import Thread
import npyscreen


class LoadingForm(npyscreen.ActionForm):
    '''Questa classe gestisce il form di caricamento della GUI.'''

    def create(self):
        '''Questo è il metodo di definizione e creazione degli elementi grafici della pagina Loading.'''
        self.loading_text = self.add(
            npyscreen.TitleText, name="Loading...", w_id="loading")
        self.loading_text.set_relyx(
            self.loading_text.rely + 7, self.loading_text.relx + 90)
        self.loading_text.max_height = 3
        self.add_handlers({
            "^X": self.on_quit,
        })
        self.listener = Thread(target=self.listen)
        self.listener.start()

    def listen(self):
        '''Questo metodo continua a controllare se self.feeds viene popolato.'''
        feed_is_empty: bool = True
        while feed_is_empty:
            sleep(0.1)
            self.parentApp.mutex.acquire()
            feed_is_empty = self.parentApp.feeds is None
            self.parentApp.mutex.release()
        self.loading_text.value = "Loading complete!"
        self.parentApp.switchForm("BROWSER")
        self.display()

    def on_quit(self, _) -> None:
        '''Questo metodo gestisce la chiusura dell'applicazione.'''
        self.parentApp.switchForm(None)
