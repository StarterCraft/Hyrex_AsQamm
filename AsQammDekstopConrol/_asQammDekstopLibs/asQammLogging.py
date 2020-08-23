import logging, time, os

class AqLogger:

    def __init__(self, name):

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

    def openLogFolder(self):
        os.system('explorer "log"')
        self.Logger.debug('Инициирована попытка открыть папку log')
