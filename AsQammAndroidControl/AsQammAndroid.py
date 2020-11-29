# импорт модулей
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.toast import toast

from libs.server import AqServerCommutator
from libs.functions import AqCrypto, AqThread
from libs.logging import AqLogger

import requests

import json

class Root(AnchorLayout): # главный класс приложения
    
    scr_mngr = ObjectProperty(None)

    def checkingLogin(self):
        username = self.scr_mngr.login_screen.username.text
        password = self.scr_mngr.login_screen.password.text


        if username.replace(" ", "") == "" and password.replace(" ", "") == "":
           self.server.commutatorLogger.info("Введите логин и пароль")
           toast("Введите логин и пароль")

        elif username.replace(" ", "") == "":
            self.server.commutatorLogger.info("Введите логин")
            toast("Введите логин")

        elif password.replace(" ", "") == "":
            self.server.commutatorLogger.info("Введите пароль")
            toast("Введите пароль")

        else:
            self.change_screen("loading")

            try:
                userData = self.server.get('getUserdata', json)
                rg = self.server.get('getUserRg', json)
            except requests.exceptions.ConnectionError:
                self.server.commutatorLogger.info("Сервер не найден")
                self.change_screen("setupServer")
                return

            users = [i for i in userData if i['login'] == username]

            self.isSign = False

            if len(users):
                for i in rg:
                    if users[0]['password'] == self.crypto.getCut(password, bytes.fromhex(i)):
                        self.server.commutatorLogger.info("вы вОшЛЫ! ЫыЫы")
                        self.isSign = True
                        break

            if not isSign:
                self.server.commutatorLogger.info("логин ИЛИ пароль неверный, ВоЗМоЖНО Вы ТУпЫе")
                self.change_screen("login_screen")

    def checkDataLogin(self):
        thread = AqThread(target=self.checkingLogin)
        thread.start()

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
