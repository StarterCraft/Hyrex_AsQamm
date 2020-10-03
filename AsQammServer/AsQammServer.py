import uvicorn, py3rijndael
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request
from pyfirmata import (Arduino     as ArduinoUno,
                       ArduinoMega as ArduinoMega,
                       util        as ArduinoUtil)
from random import uniform

from _asQammServerLibs.functions import *
from _asQammServerLibs.users import *


class AqServer:
    def __init__(self):
        self.api = FastAPI()
        self.serverLogger = AqLogger('Server')
        self.crypto = AqCrypto()
        self.tok = AqTokChecker()
        
        self.authorizedInstances = []
        self.mkdirs()

        self.serverLogger.info('Проверка файлов окружения')
        self.mkreg()
        self.mkffd()


    def mkdirs(self):
        neededDirs = ['/log', '/data', '/data/personal', '/data/config', '/data/system']
        self.serverLogger.info('Проверка директорий окружения')
        rootdir = os.getcwd()

        for i in neededDirs:
            try:
                os.makedirs(str(rootdir + i))
            except FileExistsError:
                continue


    def mkreg(self):
        try:
            with open('data/system/ffreg32.sz', 'x') as dataFile:
                dataFile.write(self.crypto.encryptContent('[]'))
        except FileExistsError:
            pass


    def mkffd(self):
        try:
            with open('data/ffd32.bin', 'xb') as dataFile:
                dataFile.write('[]')
        except FileExistsError:
            pass


    def run(self, ip: str, _port: int):
        uvicorn.run(self.api, host = ip, port = _port)


if __name__ == '__main__':
    IP = input(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите IP-адрес для запуска: ')
    portstr = input(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите порт сервера для запуска: ')

    server = AqServer()
    userCore = AqUserSystem()

    server.serverLogger.info('Привязка глобальных методов сервера')
    @server.api.get('/getUserdata', description = 'Получить словарь данных пользователей')
    def getUserdata(data: dict, request: Request):
        global server

        try:
            if server.tok.isOk(data['tok']):
                server.serverLogger.debug(f'Вызван метод /getUserdata со стороны клиента {request.client.host}:{request.client.port}')
                return userCore.getUserData()
            elif not server.tok.isOk(data['tok']):
                return {'401': 'UNAUTHORIZED'}
        except KeyError:
            return {'401': 'UNAUTHORIZED'}


    @server.api.get('/getUserRg', description = 'Получить внешний регистр')
    def getUserRg(data: dict, request: Request):
        global server

        try:
            if server.tok.isOk(data['tok']):
                server.serverLogger.debug(f'Вызван метод /getUserRg со стороны клиента {request.client.host}:{request.client.port}')
                return userCore.getUserRegistry()
            elif not server.tok.isOk(data['tok']):
                return {'401': 'UNAUTHORIZED'}
        except KeyError:
            return {'401': 'UNAUTHORIZED'}


    @server.api.get('/getNewUserFilename', description = 'Получить новое случайное имя файла для нового аккаунта пользователя')
    def getNewUserFilename(data: dict, request: Request):
        global server

        try:
            if server.tok.isOk(data['tok']):
                server.serverLogger.debug(f'Вызван метод /getNewUserFilename со стороны клиента {request.client.host}:{request.client.port}')
                return userCore.getFilenameForNewUser()
            elif not server.tok.isOk(data['tok']):
                return {'401': 'UNAUTHORIZED'}
        except KeyError:
            return {'401': 'UNAUTHORIZED'}


    @server.api.post('/updateUserdata', description = 'Обновить словарь данных пользователей')
    def updateUserdata(object: dict, request: Request):
        global server

        try:
            if server.tok.isOk(object['tok']):
                server.serverLogger.debug(f'Вызван метод /updateUserdata со стороны клиента {request.client.host}:{request.client.port}')
                userCore.updateUserData(object['data'])
            else:
                return {'401': 'UNAUTHORIZED'}
        except KeyError:
            return {'401': 'UNAUTHORIZED'}


    @server.api.post('/updateUserRg', description = 'Обновить внешний регистр')
    def updateUserRg(object: dict, request: Request):
        global server

        try:
            if server.tok.isOk(data['tok']):
                server.serverLogger.debug(f'Вызван метод /updateUserRg со стороны клиента {request.client.host}:{request.client.port}')
                userCore.updateUserRegistry((object['data'])[1], (object['data'])[0])
            else:
                return {'401': 'UNAUTHORIZED'}
        except KeyError:
            return {'401': 'UNAUTHORIZED'}


    @server.api.delete('/delUserAcc', description = 'Удалить аккаунт пользователя (пользователей)')
    def delUserAcc(object: dict, request: Request):
        global server

        try:
            if server.tok.isOk(data['tok']):
                server.serverLogger.debug(f'Вызван метод /delUserAcc со стороны клиента {request.client.host}:{request.client.port}')
                userCore.deleteUserAccount(object['data'])
            else:
                return {'401': 'UNAUTHORIZED'}
        except KeyError:
            return {'401': 'UNAUTHORIZED'}


    server.serverLogger.info('Запуск главного цикла сервера')
    server.run(IP, int(portstr))
