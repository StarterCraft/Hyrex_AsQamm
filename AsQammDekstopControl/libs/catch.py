'''
Модуль работы с критичекими ошибками.
Используются наработки @Eugeny из 2013 года
===
Последний раз обновлялся: обновление 96, дата изменения: 20 января 2021
'''

from libs            import VERSION
from libs.exceptions import *
from collections     import namedtuple
from subprocess      import Popen
from datetime        import datetime
from colorama        import Fore, Style

import sys, time, inspect


class AqCrashHandler:
    '''
    Внутренний обработчик критических ошибок, которые приводят к закрытию программы.
    Вступает в дело, если код не можнт обработать исключение самостоятельно. Формирует
    подробный отчёт об ошибке, сохраняет его в папке с отчётами и вызывает внешний
    обработчик.
    ===
    Последний раз обновлялся: обновление 96, дата изменения: 19 января 2021
    '''

    maxDepth = 5
    framesQty = 0
    framesWithoutLocals = []
    localsFormatted = False
    saveTo = 'crashReports/'

    codes = {'ServerConnectionError': 'SCF404',
             'Other': 'UND000'}

    ignoreTypes = True
    ignoreVarnames  = True

    ignoredTypes = ['type', 'function', 'method', 'module', 'wrappertype', 'sip.wrappertype',
                    'DockOption', 'enumtype', 'enum.EnumMeta', 'RenderFlag', 'PaintDeviceMetric',
                    'pyqtBoundSignal', 'PyQt5.QtCore.QtMsgType',
                    'colorama.ansi.AnsiFore', 'colorama.ansi.AnsiStyle']

    ignoredVarnames = ['function', 'method', 'exception', 'qt_resource_data', 'qt_resource_name', 
                       'qt_resource_struct_v1', 'qt_resource_struct_v2', 'qt_resource_struct',
                       'PYQT_VERSION', 'QT_VERSION', 'qt_version', 'rcc_version']

    Report = namedtuple('Report', ['crashLoc', 'crashLocVr',
                                   'logFile', 'excCode', 'errData',
                                   'timestamp', 'exception', 'traceback'])
    Frame = namedtuple('Frame', ['file', 'line', 'code', 'locals', 'srclines'])


    @staticmethod
    def collectFrame(frame) -> Frame:
        '''
        Построить сервисный объект кадра трассировки. Используется в collect()
        
        :param 'frame': кадр трассировки tb.tb_frame
        :returns: Frame
        '''
        return AqCrashHandler.Frame(
            file = inspect.getfile(frame),
            line = frame.f_lineno,
            locals = frame.f_locals,
            code = frame.f_code,
            srclines = inspect.getsourcelines(frame)
        )


    def setupIgnorance(self, varnamesIgnorance: bool = True, typesIgnorance: bool = True,
                       addVarnames: tuple = tuple(), addTypes: tuple = tuple(),
                       removeVarnames: tuple = tuple(), removeTypes: tuple = tuple(),
                       rewriteVarnames: bool = False, rewriteTypes: bool = False): 
        '''
        Изменить правила игнорирования локальных переменных (или атрибутов, далее — 
        переменных) по именам переменных или типам данных (классам объектов) значений
        этих переменных при форматировании отчёта об ошибке. Все аргументы используют
        ключевые слова. Вызов функции без них не изменит настройки.

        !   B   Н   И   М   А   Н   И   Е   !
        Настоятельно не рекомендую отключать оба параметра varnamesIgnorance и
        typesIgnorance. Это создаст огромное количество бесполезных данных о локальных
        переменных в отчёте об ошибке, в том числе будут описаны все атрибуты модулей,
        которые импортированы в код.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        :param 'varnamesIgnorance': bool
            Включить/отключить игнорирование заданных имён переменных

        :param 'varnamesIgnorance': bool
            Включить/отключить игнорирование заданных типов данных (классов
            объектов) в переменных

        :param 'addVarnames': tuple
            Добавить в текущий список игнорируемых имён переменных содержимое
            кортежа. Уже заданные имена НЕ ПЕРЕЗАПИСЫВАЮТСЯ

        :param 'addTypes': tuple
            Добавить в текущий список игнорируемых типов данных (классов
            объектов) в переменных содержимое кортежа. Уже заданные типы
            НЕ ПЕРЕЗАПИСЫВАЮТСЯ

        :param 'removeVarnames': tuple
            Убрать из текущего списка игнорируемых имён переменных содержимое
            кортежа

        :param 'removeTypes': tuple
            Убрать из текущего списка игнорируемых типов данных (классов
            объектов) переменных содержимое кортежа

        :param 'rewriteVarnames': bool
            Если True, текущий список игнорируемых имён переменных будет
            ПЕРЕЗАПИСАН. Если этот параметр использовать вместе с 'addVarnames',
            то имена из последнего будут добавлены в текущий список
            игнорируемых имён переменных
        
        :param 'rewriteTypes': bool
            Если True, текущий список игнорируемых типов данных (классов
            объектов) в переменных будет ПЕРЕЗАПИСАН. Если этот параметр
            использовать вместе с 'addTypes', то имена из последнего будут
            добавлены в текущий список игнорируемых типов данных (классов
            объектов)

        :returns: None
        '''

        self.ignoreVarnames, self.ignoreTypes = varnamesIgnorance, typesIgnorance

        if rewriteVarnames: self.ignoredVarnames.clear()
        if rewriteTypes: self.ignoredTypes.clear()

        if addVarnames: self.ignoredVarnames.extend(addVarnames)
        if addTypes: self.ignoredTypes.extend(addTypes)

        if removeVarnames: 
            for varnameToRemove in removeVarnames:
                try: self.ignoredVarnames.remove(varnameToRemove)
                except Exception as exception: continue

        if removeTypes:
            for varnameToRemove in removeVarnames:
                try: self.ignoredVarnames.remove(varnameToRemove)
                except Exception as exception: continue
            

    def isValidToRepresent(self, varname: str, object) -> bool:
        '''
        Проверить, язвляется ли переменная/атрибут 'varname' и значение
        'object' допустимыми для того, чтобы они упоминались в списке
        локальных переменных в отчёте об ошибке. Возвращает True или False
        в зависимости от результата проверки

        Происходит итерация по спискам self.ignoreVarnames и
        self.ignoreTypes, в процессе которой проверяется, есть ли
        'varname' в self.ignoreVarnames и есть ли str(type('object'))
        в self.ignoreTypes. Если хотя бы одно из этих условий соблюдено,
        возвращается False, иначе — True.

        :param 'varname': str
            Имя переменной/атрибута

        :param 'object': Any
            Сам объект (предоставляем для проверки типа данных (класса
            объекта))

        :returns: bool
        '''
        if not (varname in ('self', 'e') or varname.startswith('__')):
            if self.ignoreVarnames:
                for t in self.ignoredTypes:
                    if ((t in str(type(object))[7:-1]) or
                        (t == str(type(object))[7:-1])):
                        return False

            if self.ignoreTypes:
                for vn in self.ignoredVarnames:
                    if ((vn in varname) or
                        (vn == varname)):
                        return False

                else: return True


    def extractAttrs(self, object) -> dict:
        '''
        Представить атрибуты льбого объекта как словарь, если имя и тип
        втрибута соответствуют правилам игнорирования (см. документацию
        к методaм isValidToRepresent и setupIgnorance).
        
        :param 'object': Any
        :returns: dict
        '''
        result = {}
        for k in dir(object):
            if (hasattr(object, k)): 
                if self.isValidToRepresent(k, getattr(object, k)):
                    result[k] = getattr(object, k)
        return result


    def collect(self, exception: Exception, logFileAddr: str, exceptionData: tuple = tuple(),
                crashLocation: str = 'AsQamm Dekstop') -> Report:
        '''
        Первоначальная функция для работы с исключением. Формирует объект
        Report для дальнейшего формирования отчёта об ошибке. Используются
        наработки достопочтенного @Eugeny (https://github.com/Eugeny).

        :param 'exception': Exception
            Объект исключения, который нужно обработать

        :param 'logFileAddr': str
            Адрес текущего файла лога сессии

        :param 'exceptionData': tuple
            Параметр используется для получения обработчиком информации,
            специфичной для конкретной ошибки. Пока не используется

        :param 'crashLocation': str
            Компонент системы AsQamm, в котором произошла ошибка.

        :returns: Report
        '''
        traceback, exceptionCode, _exceptionData = [], '', []

        if hasattr(exception, 'tracebackBackup'):
            tb = exception.tracebackBackup
        else:
            excInfo = sys.exc_info()
            tb = excInfo[2]

        while tb:
            frame = tb.tb_frame
            traceback.append(self.collectFrame(frame))
            tb = tb.tb_next

        for excType, excCode in self.codes.items():
            if exception.__class__.__name__ == excType:
                exceptionCode = excCode
                break
        else: exceptionCode = self.codes['Other']

        if hasattr(exception, 'data'): _exceptionData.extend(getattr(exception, 'data'))
        for item in exceptionData: _exceptionData.append(f'"{item}"')

        return self.Report(
            crashLoc   = crashLocation,
            crashLocVr = VERSION,
            logFile    = logFileAddr,
            timestamp  = time.time(),
            exception  = exception,
            traceback  = traceback,
            excCode    = exceptionCode,
            errData    = _exceptionData
        )


    def formatTracebackFrame(self, frame) -> str:
        '''
        Преобразует кадр трассировки критического исключения в строку,
        отмечая особым образом строку, в которой было вызвано исключение.
        Используются наработки достопочтенного @Eugeny
        (https://github.com/Eugeny).

        :param 'frame': Frame
            Кадр трассировки критического исключения

        :returns: str
        '''
        if self.localsFormatted:
            self.framesQty += 1
            self.localsFormatted = False

        lines, firstLineNo = frame.srclines

        #firstLineNo (то же, что и excLine) — номер первой строки блока исходного кода (если выполнялась
        #             функция, то номер строки с определением функции. Иначе — первая строка модуля — 0)
        #frame.line — строка, в которой было вызвано исключение

        excLine = frame.code.co_firstlineno

        preparedLines = []
        code = '‖   |'

        i = firstLineNo
        for line in lines:
            i += 1
            if i in range(frame.line - 8, frame.line + 9):
                if i == frame.line: preparedLines.append(f'>>> {line}')
                else: preparedLines.append(f'    {line}')
            
        code += '‖   |'.join(preparedLines)

        return '''@ %(file)s, строка %(line)s (кадр #%(frameNo)s):
%(code)s‖
''' % {
            'file': frame.file,
            'line': frame.line,
            'frameNo': self.framesQty,
            'code': code,
        }


    def formatLocals(self, frame) -> str:
        '''
        Извлекает информацию о локальных переменных из кадра
        трассировки критического исключения в строку, которая
        является списком локальных переменных и их значений.
        Если имена или значения переменных подпадают под
        правила игнорирования, они не включаются в этот список.

        :param 'frame': Frame
            Кадр трассировки критического исключения

        :returns: str
        '''
        i = int()
        localsText = f'@ кадр #{self.framesQty}:\n'

        for varname, value in frame.locals.items():
            if self.isValidToRepresent(varname, value):
                if type(value) == dict:
                    localsText += f'''‖   |   {varname} ({type(value).__name__}):\n'''
                    for k, v in value.items():
                        if self.isValidToRepresent(k, v): localsText += f'''‖   |   |    "{k}": {v}\n'''
                    localsText += '‖   |\n'
                    i += 1


                elif hasattr(value, '__dict__') and ('class' in str(type(value))):
                    localsText += f'''‖   |   {varname} (object of type {str(type(value))[7:-1]}):\n'''

                    d = self.extractAttrs(value)
                    for k, v in d.items():
                        localsText += f'''‖   |   |   attribute '{k}' ({type(v).__name__}): {v}\n'''
                    localsText += '‖   |\n'
                    i += 1


                else:
                    localsText += f'''‖   |   {varname} ({type(value).__name__}): {repr(value)}\n'''
                    i += 1


        self.localsFormatted = True
        if i: return localsText
        else: return ''


    def format(self, report: Report) -> str:
        '''
        Представляет объект Report как строку отчёта об ошибке,
        готовую к сохранению в файл.
        Используются наработки достопочтенного @Eugeny
        (https://github.com/Eugeny).
        
        В отчёт включаются:
        — Наименование части AsQamm, в которой произошла ошибка;
        — Версия части AsQamm, в которой произошла ошибка;
        — Точное время возникновения критической ошибки;
        — Наименование и сообщение исключения;
        — Трассировка по кадрам;
        — Локальные переменные по кадрам

        :param 'report': Report
            Объект Report (см. документацию к методу collect)

        :returns: str
        '''
        tracebackAsList, localsAsList = [], []
        emptyLocalsMessage = ''

        for frame in report.traceback:
            tracebackAsList.append(self.formatTracebackFrame(frame))

            localsForFrame = self.formatLocals(frame)
            if localsForFrame: localsAsList.append(localsForFrame)
            else: self.framesWithoutLocals.append(frame)

        if self.framesWithoutLocals:
            messagePart = ''
            for frameNo in range(len(self.framesWithoutLocals)):
                messagePart += f'{frameNo}, '
            messagePart = messagePart[:-2]
            emptyLocalsMessage = f'\n‖   Кадры {messagePart} не содержат локальных переменных'

        return '''================================
| Отчёт об ошибке Hyrex AsQamm |
================================
Отчёт об о ошибке сгенерирован с использованием кода Python Catcher от Eugene Pankow, v0.1.5

Произошла критическая ошибка в %(crashLoc)s версии %(crashLocVersion)s;
исключение произошло %(timestamp)s, сообщая следующее:
‖   %(exceptionName)s: %(exceptionDesc)s

Трассировка:
‖   %(traceback)s

Локальные переменные:%(emptyLocals)s
‖   %(locals)s
        ''' % {
            'timestamp': datetime.fromtimestamp(int(report.timestamp)),
            'crashLoc': report.crashLoc,
            'crashLocVersion': report.crashLocVr,
            'traceback': '‖   '.join(tracebackAsList),
            'locals': '‖   '.join(localsAsList),
            'emptyLocals': emptyLocalsMessage,
            'exceptionName': type(report.exception).__name__,
            'exceptionDesc': str(report.exception),
        }


    def handle(self, exception: Exception, logFileAddr: str):
        '''
        Обработать критическую ошибку. Вызывается при возникновении
        исключения. Создаёт отчёт об ошибке и сохраняет его в файл
        '{self.saveTo}/{время ошибки}_AsQammCrash.log', после чего
        вызывает внешний обработчик ошибок AsQammCrashHandler

        :param 'exception': Exception
            Экземпляр исключения.
            
        :param 'logFileAddr': str
            Адрес текущего файла лога сессии
        '''
        crashReport = self.collect(exception, logFileAddr)
        crashReportText = self.format(crashReport)
        crashReportFileAddr = f'{self.saveTo}{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammCrash.log'

        with open(crashReportFileAddr, 'w', encoding = 'utf-8') as reportFile:
           reportFile.write(crashReportText)

        print(f'[{Fore.GREEN}Core{Style.RESET_ALL}@{Fore.RED}CRITICAL{Style.RESET_ALL}]: не удалось '
              f'обработать критическое исключение {exception.__class__.__name__}')

        Popen(f'AsQammCrashHandler "{crashReport.crashLoc}" "{crashReportFileAddr}" '
              f'"{crashReport.excCode}" "{crashReport.logFile}" {" ".join(crashReport.errData)}')
        return
