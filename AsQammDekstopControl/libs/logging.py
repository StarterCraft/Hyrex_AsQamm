import logging, time, os, platform, traceback
from colorama import Fore as Fore, Style as Style, init as initColorama
initColorama()

sessionLogFilename = f'logs/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammLog.log'


class AqLogger:
    '''
    Класс канала журналирования.

    Журналирование необходимо для отборажения пользователю информацию о 
    текущих действиях сервера, сообщения о предупреждениях и об ошибках.

    Каналов журналирования (или `логгеров`) может быть сколько угодно.
    При этом итоговый журнал всегда сохраняется в ОДИН файл, имя которого
    определяется при запуске самого ПЕРВОГО канала журналирования.
    Каждый из этих каналов имеет своё имя и настраивается по уровню жур-
    налирования (насколько важные сообщения нужно выводить в консоль и
    сохранять в журнал?).

    Любые файлы журналов сохраняются в папке
    '{папка местонаждения программы}/logs'.
    '''
    class LogLevel:
        'Объект для представления уровня журналирования'
        def __init__(self, lm: int):
            self._level = lm


        def __repr__(self):
            repr(self._level)


        def __eq__(self, other):
            if not hasattr(other, '_level'):
                return self._level == other
            else: return self._level == other._level


        def __gt__(self, other):
            if not hasattr(other, '_level'):
                return self._level > other
            else: return self._level > other._level


        def __lt__(self, other):
            if not hasattr(other, '_level'):
                return self._level < other
            else: return self._level < other._level


        def __ge__(self, other):
            if not hasattr(other, '_level'):
                return self._level >= other
            else: return self._level >= other._level


        def __le__(self, other):
            if not hasattr(other, '_level'):
                return self._level <= other
            else: return self._level <= other._level


    #Возможные уровни журналирования:
    DEBUG = LogLevel(logging.DEBUG)       #Уровень ОТЛАДКА (все сообщения, по умолчанию)
    INFO = LogLevel(logging.INFO)         #Уровень ИНФОРМАЦИЯ (важные сообщения)

    WARNING = LogLevel(logging.WARNING)   #Уровень ПРЕДУПРЕЖДЕНИЯ (сообщения важностью
                                          #ПРЕДУПРЕЖДЕНИЕ и выше)

    ERROR = LogLevel(logging.ERROR)       #Уровень ОШИБКИ (только сообщения об ошибках и
                                          #критические сообщения)

    CRITICAL = LogLevel(logging.CRITICAL) #Уровень ТОЛЬКО КРИТИЧЕСКИЕ (только критические
                                          #сообщения)


    def __init__(self, name: str, logLevel: LogLevel = self.DEBUG,
                                  disableStdPrint: bool = False,
                                  useColorama: (0, 1, 2) = 1):
        '''
        Инициализировать один канал журналирования.

        :param 'name': str
            Имя канала журналирования

        :param 'logLevel': AqLogger.LogLevel = DEBUG
            Необходимый уровень журналирования.

            Возможные уровни журналирования:
             —— DEBUG (все сообщения, по умолчанию);
             —— INFO (важные сообщения);
             —— WARNING (сообщения важностью 
                ПРЕДУПРЕЖДЕНИЕ и выше);
             —— ERROR (только сообщения об ошибках и
                критические сообщения);
             —— CRITICAL (только критические сообщения)

        :param 'disableStdPrint': bool = False
            По умолчанию, сообщения журнала выводятся в консоль.
            Если этот параметр ложен, то вывод в консоль не будет
            производиться

        :param 'useColorama': int = 1
            Использовать ли цветной текст Colorama, и если да, то
            как. Имеются следующие варианты:
            0 —— отключить использование цветного текста;
            1 —— использовать цветной текст для вывода
                 сообщений в консоль;
            2 —— использовать цветной текст для вывода
                 сообщений в консоль и для файла журнала
        '''
        self.name, self.logLevel, self.printDsb, self.useColorama = name, logLevel, disableStdPrint, useColorama
        self.filenames = list()

        self.Logger = logging.getLogger(name)
        self.getFilename()
        
        self.Logger.setLevel(self.logLevel._level)

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            formatter = logging.Formatter('{%(asctime)s} [%(name)s:%(levelname)s] [%(filename)s <%(lineno)s>: '
                                          '%(module)s.%(funcName)s]: %(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            formatter = logging.Formatter('{%(asctime)s} [%(name)s:%(levelname)s] [%(module)s.%(funcName)s]: '
                                          '%(message)s')

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            formatString = (Fore.CYAN   + ' {%(asctime)s} [' + Style.RESET_ALL +
                            Fore.GREEN  +   '%(name)s'       + Style.RESET_ALL + ':'   +
                            Fore.YELLOW +   '%(levelname)s'  + Style.RESET_ALL + '] [' +
                            Fore.BLUE   +   '%(filename)s'   + Style.RESET_ALL + ' <'  +
                            Fore.WHITE  +   '%(lineno)s'     + Style.RESET_ALL + '>: ' +
                            Fore.BLUE   +   '%(module)s'     + Style.RESET_ALL + '.'   +
                                            '%(funcName)s]: %(message)s')

            formatter = logging.Formatter(formatString)
        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            formatString = (Fore.CYAN   + ' {%(asctime)s} [' + Style.RESET_ALL +
                            Fore.GREEN  +   '%(name)s'       + Style.RESET_ALL + ':'   +
                            Fore.YELLOW +   '%(levelname)s'  + Style.RESET_ALL + '] [' +
                            Fore.BLUE   +   '%(module)s'     + Style.RESET_ALL + '.'   +
                                            '%(funcName)s]: %(message)s')

            formatter = logging.Formatter(formatString)

        handler = logging.FileHandler(rf'{self.filenames[0]}', 'a+', 'utf-8')
        handler.setFormatter(formatter)

        self.Logger.addHandler(handler)


    def setLogLevel(self, logLevel: LogLevel):
        '''
        Установить уровень журналирования.

        :param 'logLevel': AqLogger.LogLevel
            Необходимый уровень журналирования.

            Возможные уровни журналирования:
             —— DEBUG (все сообщения, по умолчанию);
             —— INFO (важные сообщения);
             —— WARNING (сообщения важностью 
                ПРЕДУПРЕЖДЕНИЕ и выше);
             —— ERROR (только сообщения об ошибках и
                критические сообщения);
             —— CRITICAL (только критические сообщения)

        :returns: None
        '''
        self.logLevel = logLevel
        self.Logger.setLevel(logLevel._level)


    def getFilename(self):
        self.filenames.append(f'logs/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammLog.log')


    def debug(self, message: str):
        '''
        Опубликовать сообщение с уровнем DEBUG (ОТЛАДКА).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        self.Logger.debug(message)
        if self.logLevel == self.DEBUG and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}DEBUG{Style.RESET_ALL}]: {message}')
        

    def info(self, message: str):
        '''
        Опубликовать сообщение с уровнем INFO (ИНФОРМАЦИЯ).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        self.Logger.info(message)
        if self.logLevel <= self.INFO and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}INFO{Style.RESET_ALL}]: {message}')


    def warning(self, message: str):
        '''
        Опубликовать сообщение с уровнем WARNING (ПРЕДУПРЕЖДЕНИE).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        self.Logger.warning(message)
        if self.logLevel <= self.WARNING and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}WARN{Style.RESET_ALL}]: {message}')


    def error(self, message: str):
        '''
        Опубликовать сообщение с уровнем ERROR (ОШИБКА).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        self.Logger.error(message)
        if self.logLevel <= self.ERROR and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}ERROR{Style.RESET_ALL}]: {message}')


    def critical(self, message: str):
        '''
        Опубликовать сообщение с уровнем CRITICAL (КРИТИЧЕСКИЙ).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        self.Logger.critical(message)
        if self.logLevel <= self.CRITICAL and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: {message}')


    def exception(self, _exception: Exception):
        '''
        Опубликовать сообщение о возникновении исключения

        :param '_exception': Exception
            Объект исключения.

        :returns: None
        '''
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: '
              f'Программа аварийно завершила работу из-за исклоючения {type(exception)}:')
        self.Logger.exception(f'Программа аварийно завершила работу из-за исклоючения {type(exception)}:',
                                exc_info = _exception)


    def openLogFolder():
        '''
        Открыть папку с файлами журналов.

        :returns: None
        '''
        os.system('explorer logs')

