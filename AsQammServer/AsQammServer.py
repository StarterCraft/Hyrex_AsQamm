import uvicorn, socket, subprocess, threading

from typing             import Optional
from pydantic           import BaseModel
from fastapi            import FastAPI, Request
from random             import uniform
from sys                import (argv as sysArgs,
                                exit as exit)

from libs.functions     import *
from libs.users         import *
from libs.hardware      import *
from PyQt5.QtWidgets    import QApplication


class AqServer:
    def __init__(self):
        self.api = FastAPI()
        self.serverLogger = AqLogger('Core')
        self.crypto = AqCrypto()
        self.tok = AqTokChecker()
        self.authorizedInstances = []
        self.publishViaNgrok = False

        self.serverLogger.info('Инициализация')
        self.mkdirs()

        self.serverLogger.debug('Проверка файлов окружения')
        self.mkreg()
        self.mkffd()


    def mkdirs(self):
        neededDirs = ['/logs', '/crashReports', '/data', '/data/personal', '/data/config', '/data/system']
        self.serverLogger.debug('Проверка директорий окружения')
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
        if self.publishViaNgrok:
            self.serverLogger.info('Запуск сессии Ngrok...')
            threading.Thread(target = self.publish, args = [_port]).start()
  
        try:
            uvicorn.run(self.api, host = ip, port = _port)
        except ValueError:
            if ip.replace(' ', '').lower() == 'localhost':
                uvicorn.run(self.api, host = socket.gethostbyname(socket.gethostname()), port = _port)


    def publish(self, _port: int):
        with open('data/config/~!ngrokconfig!~.asqd', 'r') as configFile:
            configData = (json.loads(self.crypto.decryptContent(configFile.read())))
            subprocess.Popen(f'{configData["executable"]} authtoken {configData["authtoken"]}',
                                creationflags = subprocess.CREATE_NEW_CONSOLE)

            subprocess.Popen(f'{configData["executable"]} http {_port}',
                                creationflags = subprocess.CREATE_NEW_CONSOLE)
                

if __name__ == '__main__':
    try:
        hardware = None
        runningMode = None

        # Определим, запускаемся ли из оболочки Python или из exe
        if sysArgs[0].endswith('.py'):
            runningMode = 'PYTHONENV'
        else:
            runningMode = 'EXE'


        if len(sysArgs) < 2:
            print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите IP-адрес для запуска: ', end = '')
            IP = input()

            print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите порт сервера для запуска: ', end = '')
            portstr = input()
        
            print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Нажмите {Fore.CYAN}ENTER{Style.RESET_ALL}'
                  f' для запуска сервера в обычном режиме или используйте аргументы:\n'
                  f'                 | "{Fore.CYAN}-h{Style.RESET_ALL}" или "{Fore.CYAN}--nohardware{Style.RESET_ALL}" '
                  f'для запуска сервера в режиме совместимости без оборудования;\n'
                  f'                 | "{Fore.CYAN}-n{Style.RESET_ALL}" или "{Fore.CYAN}--ngrok{Style.RESET_ALL}" '
                  f'для вывода сервера в Интернет через ngrok')
            addArgs = input(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}PROMPT{Style.RESET_ALL}]: ').split(' ')


        elif len(sysArgs) < 3:
            IP = sysArgs[1]

            print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите порт сервера для запуска: ', end = '')
            portstr = input()

            print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Нажмите {Fore.CYAN}ENTER{Style.RESET_ALL}'
                  f' для запуска сервера в обычном режиме или используйте аргументы:\n'
                  f'                 | "{Fore.CYAN}-h{Style.RESET_ALL}" или "{Fore.CYAN}--nohardware{Style.RESET_ALL}" '
                  f'для запуска сервера в режиме совместимости без оборудования;\n'
                  f'                 | "{Fore.CYAN}-n{Style.RESET_ALL}" или "{Fore.CYAN}--ngrok{Style.RESET_ALL}" '
                  f'для вывода сервера в Интернет через ngrok')
            addArgs = input(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}PROMPT{Style.RESET_ALL}]: ').split(' ')


        else:
            IP = sysArgs[1]
            portstr = sysArgs[2]
            addArgs = sysArgs[3:]

        server = AqServer()
        userCore = AqUserSystem()

        if (('-h' or '--hardware-offline') not in addArgs):
            hardware = AqHardwareSystem()
            assert hardware.isOk, 'Аварийное завершение работы'

        if not hardware:
            server.serverLogger.info('Сервер будет запущен без инициализации обоpудования')


        if ('-n' or '--ngrok') in addArgs: 
            server.publishViaNgrok = True


        @server.api.get('/getUserdata', description = 'Получить словарь данных пользователей')
        def getUserdata(data: dict, request: Request):
            global server

            try:
                if server.tok.isOk(data['tok']):
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
                    userCore.deleteUserAccount(object['data'])
                else:
                    return {'401': 'UNAUTHORIZED'}
            except KeyError:
                return {'401': 'UNAUTHORIZED'}
            except AttributeError:
                return {'401': 'UNAUTHORIZED'}
            except ValueError:
                return {'401': 'UNAUTHORIZED'}


        @server.api.get('/getHardwareData', description = 'Получить информацию о подключённом оборудовании, если таковое присутствует')
        def getHardwareData(data: dict, request: Request):
            global server
        
            if server.tok.isOk(data['tok']) and hardware:
                return hardware.getHardwareDataSheet()
            elif not hardware:
                return {'505': 'HARDWARE_OFFLINE'}
            else:
                return {'401': 'UNAUTHORIZED'}


        @server.api.get('/getLatestStats', description = 'Получить статистику за x времени')
        def getQueriedStats(data: dict, request: Request):
            global server

            if server.tok.isOk(data['tok']) and hardware:
                return hardware.statisticAgent.getQueriedStats(data['query'])
            elif not hardware:
                return {'505': 'HARDWARE_OFFLINE'}
            else:
                return {'401': 'UNAUTHORIZED'}

        try: hardware.startMonitoring()
        except (NameError, AttributeError): pass

        server.run(IP, int(portstr))


    except Exception as exception:
        if type(exception) == AssertionError: exit()
        else:
            from libs.catch import AqCrashHandler
            AqCrashHandler().handle(exception, sessionLogFilename)
