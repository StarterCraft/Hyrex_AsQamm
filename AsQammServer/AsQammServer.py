import uvicorn, socket, subprocess, threading, click

from typing             import Optional
from pydantic           import BaseModel
from fastapi            import FastAPI, Request
from random             import uniform
from sys                import argv, exit

from libs               import clickSettings
from libs.utils         import *
from libs.users         import *
from libs.hardware      import *
from PyQt5.QtWidgets    import QApplication


class AqServer:
    '''
    Класс ядра сервера.

    :attrib 'api': FastAPI
        Объект для работы с библиотекой FastAPI. Он осуществляет приём
        входящих запросов и вызывает функции, привязанные к ним

    :attrib 'tok': AqTokChecker
        Агент проверки токена

    :attrib 'publishViaNgrok': bool
        Если этот атрибут истинен, то при запуске сервера будет произве-
        дена попытка вывести его в Интернет с помощью NGRok
    '''
    def __init__(self):
        '''
        Конструктор ядра сервера, не принимает никаких аргументов
        '''
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


    @staticmethod
    @click.command('', context_settings = clickSettings, help = 'Запустить AsQamm Server')
    @click.option('-c', '--custom')
    def start() -> tuple:
        '''
        Метод, принимающщий аргументы (опции) от Click-a при запуске програм-
        мы. Информация о них представлена ниже:
        :returns: tuple
            Аргументы запуска программы в виде кортежа
        '''



    def mkdirs(self) -> None:
        '''
        Метод, создающий необходимые для работы прогpаммы папки в случае их
        отсутствия. Не принимает никаких аргументов.

        :returns: None
        '''
        neededDirs = ['/logs', '/crashReports', '/data', '/data/personal', '/data/config', '/data/system']
        self.serverLogger.debug('Проверка директорий окружения')
        rootdir = os.getcwd()

        for i in neededDirs:
            try: os.makedirs(str(rootdir + i))
            except FileExistsError: continue


    def mkreg(self) -> None:
        '''
        Метод, создающий пустой файл для хранения регистра пользователей,
        если он не существует, не принимает никаких аргументов.

        :returns: None
        '''
        try:
            with open('data/system/~!ffreg!~.asqd', 'x') as dataFile:
                dataFile.write(self.crypto.encryptContent('[]'))
        except FileExistsError: pass


    def run(self, ip: str, _port: int) -> None:
        '''
        Метод запуска сервера, который активирует сервер на заданном па-
        раметрами IP и порту. Если атрибут 'publishViaNgrok' истинен, то
        при запуске будет произведена попытка вывести сервер в Интернет с
        помощью NGRok (см. метод 'publish') в отдельном потоке.

        :param 'ip': str
            IP-адрес для инициализации сервера

        :param '_port': int
            № порта для инициализации сервера

        :returns: None
        '''
        if self.publishViaNgrok:
            self.serverLogger.info('Запуск сессии NGRok...')
            threading.Thread(target = self.publish, args = [_port]).start()
  
        try: uvicorn.run(self.api, host = ip, port = _port, log_level = 'debug')
        except ValueError:
            if ip.replace(' ', '').lower() == 'localhost':
                uvicorn.run(self.api, host = socket.gethostbyname(socket.gethostname()), port = _port)


    def publish(self, _port: int) -> None:
        '''
        Метод инициализации службы NGRok для вывода сервера в Интернет с
        её помощью. Для этого подгружаются параметры конфигурации из файла
        'data/config/~!config!~.asqd', где должно быть указано местоположе-
        ние исполняемого файла NGRok и токен аккаунта этой службы. Эта ин-
        формация записывается пользователем пр установке сервера или с по-
        мощью команды 'config ngrok {ПАРАМЕТР} {ЗНАЧЕНИЕ}'. Метод выполня-
        ется в отдельном потоке, инициализируемом в методе 'run'.

        :param '_port': int
            № порта, на котором инициализирован сервер

        :returns: None
        '''
        with open('data/config/~!config!~.asqd', 'r') as configFile:
            configData = json.loads(self.crypto.decryptContent(configFile.read()))
            subprocess.Popen(f'{configData["ngrok"]["executable"]} authtoken {configData["authtoken"]}',
                creationflags = subprocess.CREATE_NEW_CONSOLE)

            subprocess.Popen(f'{configData["ngrok"]["executable"]} http {_port}',
                creationflags = subprocess.CREATE_NEW_CONSOLE)


    def standardResponse(self, content) -> dict:
        '''
        Сгенерировать словарь с информацией, которую необходимо отправить
        клиенту после успешного выполнения запроса. Аргумент к этому
        методу может быть любым JSON-представляемым объектом, он и будет
        переслан клиенту.

        :param 'content': JSON-serializable
            Информация, которая должна быть передана клиенту

        :returns: dict
            Словарь для отправки в качестве ответа на запрос.
        '''        
        return {'responseCode': 200, 'content': content}


    def errorResponse(self, errorCode: int) -> dict:
        '''
        Сгенерировать словарь с кодом ошибки и её сообщением для последующей
        отправки клиенту. Используется для замены выдачи стандартной ошибки
        HTML `Internal Server Error` в случае, если при выполнении какого-то
        метода, вызванного клиентом, было поймано исключение.
        
        :attrib 'errors': dict
            Словарь, в котором содержатся коды возможных ошибок и их описания.

            {
                /*Словарь, где:
                  a —— код ошибки;
                  b —— описание ошибки
                */

                a: b,
                //другие определения ошибок по той же схеме
            }

        :param 'errorCode': int
            Код ошибки, для которой необходимо сформировать словарь с 
            описанием ошибки. Должен соответствовать допустимым кодам ошибок
            в словаре 'errors'

        :returns: dict
            Словарь для отправки в качестве ответа на запрос. Смотрите струк-
            туру ниже для дополнительной информации:

            {
                 /*Словарь, где:
                   a —— код ошибки;
                   b —— описание ошибки
                 */

                 "code": a,
                 "errorDescription": b
            }
        '''
        errors = {400: 'Bad request',
                  401: 'Unauthorized request',
                  501: 'Hardware not initialized'}
        
        return {'responseCode': errorCode,
                'error': errors[errorCode]}


if __name__ == '__main__':
    try:
        hardwareCore = None
        runningMode = None
        IP = ''
        portstr = ''
        addArgs = []

        # Определим, запускаемся ли из оболочки Python или из exe
        if argv[0].endswith('.py'):
            runningMode = 'PYTHONENV'
        else:
            runningMode = 'EXE'
            argv.insert(0, '')


        if ('-c', '--customsettings', '-h', '--help', '-?') in argv:
            try:
                IP = argv[2]
                portstr = argv[3]
                addArgs = argv[4:]

            except IndexError:
                if not IP:
                    print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите IP-адрес для запуска: ', end = '')
                    IP = input()

                if not portstr:
                    print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Введите порт сервера для запуска: ', end = '')
                    portstr = input()
        
                if not addArgs:
                    print(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}STARTUP{Style.RESET_ALL}]: Нажмите {Fore.CYAN}ENTER{Style.RESET_ALL}'
                          f' для запуска сервера в обычном режиме или используйте аргументы:\n'
                          f'                 | "{Fore.CYAN}-h{Style.RESET_ALL}" или "{Fore.CYAN}--hardware-offline{Style.RESET_ALL}" '
                          f'для запуска сервера в режиме совместимости без оборудования;\n'
                          f'                 | "{Fore.CYAN}-n{Style.RESET_ALL}" или "{Fore.CYAN}--ngrok{Style.RESET_ALL}" '
                          f'для вывода сервера в Интернет через ngrok')
                    addArgs = input(f'[{Fore.GREEN}Server{Style.RESET_ALL}@{Fore.YELLOW}PROMPT{Style.RESET_ALL}]: ').split(' ')


        else:
            with open('data/config/~!config!~.asqd', 'r') as configFile:
                configData = (json.loads(AqCrypto.decryptContent(configFile.read())))
                IP = configData['serverDefault']['ip']
                portstr = configData['serverDefault']['port']
                addArgs = argv[0:]


        server = AqServer()
        usersCore = AqUserSystem()

        if ('-h' or '--hardware-offline') not in addArgs:
            hardwareCore = AqHardwareSystem()
            assert hardwareCore.isOk

        if not hardwareCore: server.serverLogger.info('Сервер будет запущен без инициализации обоpудования')
        if ('-n' or '--ngrok') in addArgs: server.publishViaNgrok = True


        @server.api.get('/getUserdata', description = 'Получить словарь данных пользователей')
        def getUserdata(content: dict, request: Request):
            global server

            try:
                if server.tok.isOk(content['tok']): 
                    return server.standardResponse(usersCore.getUserData())
                else: return server.errorResponse(401)
            except (KeyError, AttributeError, ValueError): return server.errorResponse(401)


        @server.api.get('/getUserRg', description = 'Получить внешний регистр')
        def getUserRg(content: dict, request: Request):
            global server

            try:
                if server.tok.isOk(content['tok']):
                    return server.standardResponse(usersCore.getUserRegistry())
                else: server.errorResponse(401)
            except (KeyError, AttributeError, ValueError): return server.errorResponse(401)


        @server.api.get('/getNewUserFilename', description = 'Получить новое случайное имя файла для нового аккаунта пользователя')
        def getNewUserFilename(content: dict, request: Request):
            global server

            try:
                if server.tok.isOk(content['tok']):
                    return server.standardResponse(usersCore.getFilenameForNewUser())
                else: server.errorResponse(401)
            except (KeyError, AttributeError, ValueError): return server.errorResponse(401)


        @server.api.post('/updateUserdata', description = 'Обновить словарь данных пользователей')
        def updateUserdata(content: dict, request: Request):
            global server

            try:
                if server.tok.isOk(content['tok']):
                    usersCore.updateUserData(content['content'])
                else: server.errorResponse(401)
            except (KeyError, AttributeError, ValueError): return server.errorResponse(401)


        @server.api.post('/updateUserRg', description = 'Обновить внешний регистр')
        def updateUserRg(content: dict, request: Request):
            global server

            try:
                if server.tok.isOk(content['tok']):
                    usersCore.updateUserRegistry((content['content'])[1], (content['content'])[0])
                else: server.errorResponse(401)
            except (KeyError, AttributeError, ValueError): return server.errorResponse(401)


        @server.api.delete('/delUserAcc', description = 'Удалить аккаунт пользователя (пользователей)')
        def delUserAcc(content: dict, request: Request):
            global server

            try:
                if server.tok.isOk(content['tok']):
                    usersCore.deleteUserAccount(content['content'])
                else: server.errorResponse(401)
            except (KeyError, AttributeError, ValueError): return server.errorResponse(401)


        @server.api.get('/getHardwareData', description = 'Получить информацию о подключённом оборудовании, если таковое присутствует')
        def getHardwareData(content: dict, request: Request):
            global server, hardwareCore
            
            try:
                if server.tok.isOk(content['tok']) and hardwareCore:
                    return server.standardResponse(hardwareCore.getHardwareDataSheet())
                elif not hardwareCore: return server.errorResponse(501)
                else: server.errorResponse(401)
            except (KeyError, AttributeError, ValueError): return server.errorResponse(401)


        @server.api.get('/getLatestStats', description = 'Получить статистику за x времени')
        def getQueriedStats(content: dict, request: Request):
            global server, hardwareCore

            try:
                if server.tok.isOk(content['tok']) and hardwareCore:
                    return server.standardResponse(hardwareCore.statisticAgent.getStatsByTimeQuery(content['query']))
                elif not hardwareCore: return server.errorResponse(501)
                else: server.errorResponse(401)
            except (KeyError, AttributeError, ValueError): return server.errorResponse(401)


        try: hardwareCore.startMonitoring()
        except (NameError, AttributeError): pass

        server.run(IP, int(portstr))


    except Exception as exception:
        if type(exception) == AssertionError: exit()
        else:
            from libs.catch import AqCrashHandler
            AqCrashHandler().handle(exception, sessionLogFilename)
