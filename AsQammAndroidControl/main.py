from kivy.app import App
from kivy.uix.button import Button

class Hyrex_AsQammApp(App):
    def build(self):
        return Button(text = "Hi!") # кнопка
        
if __name__ == "__main__":
    Hyrex_AsQammApp().run()
