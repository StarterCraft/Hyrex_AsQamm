import logging, time, os, platform, traceback
from colorama import Fore as Fore, Style as Style, init as initColorama
initColorama()

sessionLogFilename = f'logs/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammLog.log'


class AqLogger:
    class LogLevel:
        DEBUG = logging.DEBUG
        INFO = logging.INFO
        WARNING = logging.WARNING
        ERROR = logging.ERROR
        CRITICAL = logging.CRITICAL


    def __init__(self, name: str, logLevel: (LogLevel.CRITICAL or LogLevel.ERROR or
                                             LogLevel.WARNING or LogLevel.INFO or
                                             LogLevel.DEBUG) = None, 
                                  useColorama: (0 or 1 or 2) = None):
        self.name = name
        self.filenames = list()
        if logLevel: self.logLevel = logLevel
        else: self.logLevel = logging.DEBUG

        self.Logger = logging.getLogger(name)
        self.getFilename()
        
        self.Logger.setLevel(self.logLevel)

        if self.logLevel == self.LogLevel.DEBUG:
            formatter = logging.Formatter('''{%(asctime)s} [%(name)s:%(levelname)s] [%(filename)s <%(lineno)s>: %(module)s.%(funcName)s]: %(message)s''')

        elif self.logLevel >= self.LogLevel.INFO:
            formatter = logging.Formatter('''{%(asctime)s} [%(name)s:%(levelname)s] [%(module)s.%(funcName)s]: %(message)s''')

        handler = logging.FileHandler(rf'{self.filenames[0]}', 'a+', 'utf-8')
        handler.setFormatter(formatter)

        self.Logger.addHandler(handler)


    def setLogLevel(self, logLevel: (LogLevel.CRITICAL or LogLevel.ERROR or
                                     LogLevel.WARNING or LogLevel.INFO or
                                     LogLevel.DEBUG)):
        self.logLevel = logLevel
        self.Logger.setLevel(logLevel)


    def getFilename(self):
        self.filenames.append(f'logs/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammLog.log')


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


    def exception(self, _exception: Exception):
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: '
              f'Программа аварийно завершила работу из-за исклоючения {type(exception)}:')
        self.Logger.exception(f'Программа аварийно завершила работу из-за исклоючения {type(exception)}:',
                                exc_info = _exception)


    def crashReport(self, exception: Exception, errorType: str, customMessage: str = None):
        with open(f'crash-reports/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammCrash.log',
                  'w', encoding = 'utf-8') as report:
            reportText = str()
            reportDict = {}

            #Время, в которое произошло обрушение
            reportDict.update({'Время', f'{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}'})

            #Краткое описание обрушения
            if errorType == 'unknown':
                reportDict.update({'Краткое описание ошибки': f'исключение {type(exception)} не было обработано из-за '
                                                              f'непредвиденной ошибки: \n{exception.message}'})

            else: reportDict.update({'Краткое описание ошибки': f'{customMessage}'})

            #Информация для обработчика ошибок
            reportDict.update({'Системная информация': '~!SYSINFO!~[{";".join([errorType, type(exception)])}]'})

            #Местоположение файла лога
            reportDict.update({'Файл журнала': f'self.filenames[0]', 'Уровень логирования': f'self.logLevel'})

            #Подробности обрушения
            reportDict.update({'Последнее сообщение от программы': traceback.format_exc()})


    def openLogFolder():
        os.system('explorer logs')
