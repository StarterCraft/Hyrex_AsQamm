import json, base64, os, glob, ffmpeg, hashlib, logging, time, secrets
from colorama import Fore as Fore, Style as Style, init as initColorama
from playsound import *
initColorama()


class AqCrypto:
    def __init__(self):
        self.cryptoLogger = AqLogger('Crypto')

    def getFileNamesList(self, exportList):

        for i in range(10, 99):
            self.initialFilename = str(r'customuser_' + str(r'{0}').format(i))
            self.initialFilename = self.initialFilename.encode('utf-8')
            self.initialFilename = base64.b64encode(self.initialFilename)
            self.initialFilename = self.initialFilename.decode('utf-8')
            self.initialFilename = self.initialFilename[0:-2]
            self.initialFilename = self.initialFilename.encode('utf-8')
            
            exportList.append(self.initialFilename)


    def seekForFiles(self, importList, exportList, flag):

        for item in importList:
                self.gotName = glob.glob(str(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8')))))

                if flag:
                    if self.gotName == []:
                        continue
                    else:
                        exportList.append(r'{0}'.format(self.gotName[0]))

                else:
                    if self.gotName != []:
                        continue
                    else:
                        exportList.append(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8'))))


    def decryptContent(self, s):
        return (base64.b64decode(s.encode('utf-8'))).decode('utf-8')


    def encryptContent(self, s):
        return (base64.b64encode(s.encode('utf-8'))).decode('utf-8')


    def getHmta(self):
        return os.urandom(32)


    def getCut(self, _str, bytes):
        print(hashlib.pbkdf2_hmac('sha256', _str.encode('utf-8'), bytes, 256256).hex())
        return (hashlib.pbkdf2_hmac('sha256', _str.encode('utf-8'), bytes, 256256).hex())


    def createInstanceToken(self):
        __sig__ = secrets.token_urlsafe(128)
        with open('data/ffd32.bin', 'rb+') as dataFile:
            fileByteString = dataFile.readline()
            fileString = fileByteString.decode('ascii')
            jsonObject = json.loads(fileString)
            jsonObject.append(str(__sig__))
        return __sig__


class AqConfig():
    def __init__(self, configDict):
        
        self.language = configDict['language']
        self.theme = configDict['theme']
        self.popupOpacity = configDict['popupOpacity']

        self.loggingMode = configDict['loggingMode']
        self.logSavingMode = configDict['logSavingMode']
        self.logSavingDuration = configDict['logSavingDuration']

        self.keyBindings = configDict['keyBindings']


    def setup(self, configDict):
        self.language = configDict['language']
        self.theme = configDict['theme']
        self.popupOpacity = configDict['popupOpacity']

        self.loggingMode = configDict['loggingMode']
        self.logSavingMode = configDict['logSavingMode']
        self.logSavingDuration = configDict['logSavingDuration']


    def setupByParam(self, param, value):
        
        if param == 'language':
            self.language = value
        elif param == 'theme':
            self.theme = value
        elif param == 'popupOpacity':
            self.popupOpacity = value

        elif param == 'loggingMode':
            self.loggingMode = value
        elif param == 'logSavingMode':
            self.logSavingMode = value
        elif param == 'logSavingDuration':
            self.logSavingDuration = value


    def setKeyBindings(self, keyBindingsDict):
        self.keyBindings = keyBindingsDict


    def getDict(self):
        return {'preset': None,
                'language': (self.language),
                'theme': (self.theme),
                'popupOpacity': (self.popupOpacity),
                'loggingMode': (self.loggingMode),
                'logSavingMode': (self.logSavingMode),
                'logSavingDuration': (self.logSavingDuration),
                'keyBindings': (self.keyBindings)}


class AqLogger:

    def __init__(self, name: str):
        self.name = name
        self.filenames = list()
        self.Logger = logging.getLogger(name)
        self.getFilename()
        
        self.Logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("""{%(asctime)s} [%(name)s:%(levelname)s] [%(filename)s <%(lineno)s>: %(module)s.%(funcName)s] %(message)s""")
        handler = logging.FileHandler((r'{0}'.format(self.filenames[0])), 'a+', 'utf-8')
        handler.setFormatter(formatter)

        self.Logger.addHandler(handler)


    def getFilename(self):
        self.filenames.append(str( 'log/' + (time.strftime("""%d.%m.%Y_%H%M%S""", (time.localtime())))  + '_AsQammLog.log'))


    def debug(self, message: str):
        self.Logger.debug(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}DEBUG{Style.RESET_ALL}]: {message}')
        

    def info(self, message: str):
        self.Logger.info(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}INFO{Style.RESET_ALL}]: {message}')


    def warning(self, message: str):
        self.Logger.warning(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}WARN{Style.RESET_ALL}]: {message}')


    def error(self, message: str):
        self.Logger.error(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}ERROR{Style.RESET_ALL}]: {message}')


    def critical(self, message: str):
        self.Logger.critical(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: {message}')
