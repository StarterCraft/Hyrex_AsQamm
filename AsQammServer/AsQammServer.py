import uvicorn, py3rijndael
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request
from random import uniform
from sys import argv as sysArgs
import socket

from _asQammServerLibs.functions import *
from _asQammServerLibs.users import *
from _asQammServerLibs.hardware import *
from PyQt5.QtWidgets import QApplication


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
            with open('data/system/~!ffreg!~.asqd', 'x') as dataFile:
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
    print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите IP-адрес для запуска: ', end = '')
    IP      = input()

    print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите порт сервера для запуска: ', end = '')
    portstr = input()

    print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Нажмите {Fore.CYAN}ENTER{Style.RESET_ALL}'
          f' для запуска сервера в обычном режиме. Введите "{Fore.CYAN}--nohardware{Style.RESET_ALL}" и нажмите {Fore.CYAN}ENTER'
          f'{Style.RESET_ALL} для запуска сервера в режиме совместимости без оборудования ', end = '')
    compart = input()

    server = AqServer()
    userCore = AqUserSystem()

    if IP.replace(" ", "") == "localhost":
        localIP = socket.gethostbyname(socket.gethostname())
        server.serverLogger.info(f'Создаётся сервер на localhost ({localIP})')

        IP = localIP

    if compart == '--nohardware':
        pass
    else:
        hardware = AqHardwareSystem()
        assert hardware.isOk

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
        except AttributeError:
            return {'401': 'UNAUTHORIZED'}
        except ValueError:
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
        except AttributeError:
            return {'401': 'UNAUTHORIZED'}
        except ValueError:
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
        except AttributeError:
            return {'401': 'UNAUTHORIZED'}
        except ValueError:
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
        except AttributeError:
            return {'401': 'UNAUTHORIZED'}
        except ValueError:
            return {'401': 'UNAUTHORIZED'}


    @server.api.post('/updateUserRg', description = 'Обновить внешний регистр')
    def updateUserRg(object: dict, request: Request):
        global server

        try:
            if server.tok.isOk(object['tok']):
                server.serverLogger.debug(f'Вызван метод /updateUserRg со стороны клиента {request.client.host}:{request.client.port}')
                userCore.updateUserRegistry((object['data'])[1], (object['data'])[0])
            else:
                return {'401': 'UNAUTHORIZED'}
        except KeyError:
            return {'401': 'UNAUTHORIZED'}
        except AttributeError:
            return {'401': 'UNAUTHORIZED'}
        except ValueError:
            return {'401': 'UNAUTHORIZED'}


    @server.api.delete('/delUserAcc', description = 'Удалить аккаунт пользователя (пользователей)')
    def delUserAcc(object: dict, request: Request):
        global server

        try:
            if server.tok.isOk(object['tok']):
                server.serverLogger.debug(f'Вызван метод /delUserAcc со стороны клиента {request.client.host}:{request.client.port}')
                userCore.deleteUserAccount(object['data'])
            else:
                return {'401': 'UNAUTHORIZED'}
        except KeyError:
            return {'401': 'UNAUTHORIZED'}
        except AttributeError:
            return {'401': 'UNAUTHORIZED'}
        except ValueError:
            return {'401': 'UNAUTHORIZED'}


    @server.api.get('/getHardwareData', description = 'Получить информацитю о подключённом оборудовании, если таковое присутствует')
    def getHardwareData(data: dict, request: Request):
        global server
        
        if server.tok.isOk(data['tok']) and hardware:
            server.serverLogger.debug(f'Вызван метод /getHardwareData со стороны клиента {request.client.host}:{request.client.port}')
            return hardware.getHardwareDataSheet()
        elif not hardware:
            return {'505': 'HARDWARE_NOT_INITIALIZED'}
        else:
            return {'401': 'UNAUTHORIZED'}


    @server.api.get('/getLatestStats', description = 'Получить статистику за x времени')
    def getLatestStats(data: dict, request: Request):
        global server

        if server.tok.isOk(data['tok']) and hardware:
            server.serverLogger.debug(f'Вызван метод /getLatestStats со стороны клиента {request.client.host}:{request.client.port}')
            return hardware.statisticAgent.getQueriedStats(data['query'])
        elif not hardware:
            return {'505': 'HARDWARE_NOT_INITIALIZED'}
        else:
            return {'401': 'UNAUTHORIZED'}

    try:
        hardware.startMonitoring()
    except NameError:
        pass

    server.run(IP, int(portstr))
