# импорт модулей
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty



import json

class Root(AnchorLayout): # главный класс приложения



    def checkDataLogin(self):
        username = self.scr_mngr.login_screen.username.text
        password = self.scr_mngr.login_screen.password.text

        userData = self.server.get('getUserdata', json)

        print(userData)


    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen
        

class Hyrex_AsQammApp(MDApp): # класс, который запускается

    title = "Hyrex_AsQamm"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        with open('ui/ui.kv', encoding='utf-8') as f:
            return Builder.load_string(f.read())

if __name__ == '__main__':
    Hyrex_AsQammApp().run() # запуск приложения
