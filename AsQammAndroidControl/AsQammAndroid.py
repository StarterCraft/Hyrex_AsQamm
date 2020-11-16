# импорт модулей
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from libs.server import AqServerCommutator
from libs.functions import AqCrypto
from libs.logging import AqLogger

import json

class Root(AnchorLayout): # главный класс приложения
    
    scr_mngr = ObjectProperty(None)

    async def checkDataLogin(self):
        username = self.scr_mngr.login_screen.username.text
        password = self.scr_mngr.login_screen.password.text

        userData = self.server.get('getUserdata', json)
        rg = self.server.get('getUserRg', json)

        users = [i for i in userData if i['login'] == username]

        isSign = False

        if len(users):
            for i in rg:
                if users[0]['password'] == self.crypto.getCut(password, bytes.fromhex(i)):
                    self.server.commutatorLogger.info("вы вОшЛЫ! ЫыЫы")
                    sign = True
                    break

        if not isSign:
            self.server.commutatorLogger.info("логин ИЛИ пароль неверный, ВоЗМоЖНО Вы ТУпЫе")


    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen
        

class Hyrex_AsQammApp(MDApp): # класс, который запускается
    
    server = AqServerCommutator()
    crypto = AqCrypto()
    title = "Hyrex_AsQamm"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        with open('ui/ui.kv', encoding='utf-8') as f:
            return Builder.load_string(f.read())

if __name__ == '__main__':
    app = Hyrex_AsQammApp()

    app.run()
