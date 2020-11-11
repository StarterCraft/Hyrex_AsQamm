import logging, time, os
from colorama import Fore as Fore, Style as Style, init as initColorama
initColorama()


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


    def openLogFolder():
        os.system('explorer log')
