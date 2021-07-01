class InvalidFirmataStringResponseError(Exception):
    '''
    Исключение вызывается, когда полученное от Arduino-
    исполнителя строковое сообщение по какой-то причине
    не соответствует синтаксису таких сообщений
    '''
    def __init__(self):
        super().__init__('От Arduino-исполнителя получено некорректное строковое сообщение')



class UndefinedCalibrationMethodError(Exception):
    '''
    Исключение вызывается, когда при инициализации Arduino-
    датчика с положительным аргументом 'isCalib' не указан
    аргумент 'clmeth'
    '''
    def __init__(self):
        super().__init__('''Не обнаружен метод калибровки 'clmeth' при инициализации Arduino-'''
                         '''датчика с возможностью калибровки. Проверьте определение класса '''
                         '''датчика''')


class DiscorrectQueryException(Exception):
    '''
    Исключение вызывается, если выборка времени для метода
    AqStatist.getStatsByTimeQuery() не соответствует синтак-
    сису этого метода (см. документацию к
    AqStatist.getStatsByTimeQuery)
    '''
    def __init__(self):
        super().__init__('При попытке получить статистику по выборке времени была получена '
                         'некорректная выборка времени')


class DuplicateQueryArgumentsException(Exception):
    '''
    Исключение вызывается, если выборка времени для метода
    AqStatist.getStatsByTimeQuery() содержит два одинаковых
    аргумента времени (см. документацию к
    AqStatist.getStatsByTimeQuery)
    '''
    def __init__(self):
        super().__init__('При попытке получить статистику по выборке времени была получена '
                         'выборка с повторяющимися аргументами времени')



