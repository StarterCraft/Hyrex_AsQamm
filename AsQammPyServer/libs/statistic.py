'''
Модуль работы со статистикой значений с датчиков.
'''

import os, glob, json
import datetime, time

from libs.utils import AqLogger


def evalMonths(monthName: str) -> int:
    '''
    Преобразовать трёхбуквенное название месяца (например, 'Jan') в номер
    этого месяца (например, 1)

    :param 'monthName': str
        Трёхбуквенное название месяца (например, 'Jan')

    :returns: int
        Номер месяца (например, 1)
    '''
    monthsStrings = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthsInts = [int for int in range(1, 13)]
    return monthsInts[(monthsStrings.index(monthName))]


def reverseMonths(monthNo: int) -> int:
    '''
    Преобразовать отрицательный номер месяца (от -11 до 0) в положительный
    номер месяца (от 1 до 12)

    :param 'monthNо': int
        Отрицательный номер месяца

    :returns: int
        Корректный номер месяца
    '''
    positiveMonths = [int for int in range(1, 13)]
    negativeMonths = [int for int in range(-11, 1)]
    return positiveMonths[negativeMonths.index(integer)]


def reverseDays(monthNo: int) -> int:
    '''
    Преобразовать отрицательный номер дня (от -32 до 0) в положительный
    номер дня (от 1 до 31)

    :param 'monthNо': int
        Отрицательный номер дня

    :returns: int
        Корректный номер дня
    '''
    positiveDays = [int for int in range(1, 32)]
    if ((int(time.strftime('%m')) - 1) == 2):
        negativeDays = [int for int in range(-29, 1)]
    else: negativeDays = [int for int in range (-32, 1)]
    return positiveDays[negativeDays.index(integer)]


def reverseHours(integer):
    '''
    Преобразовать отрицательный номер часа (от -23 до 0) в положительный
    номер часа (от 0 до 23)

    :param 'monthNо': int
        Отрицательный номер часа

    :returns: int
        Корректный номер часа
    '''
    positiveHours = [int for int in range(0, 24)]
    negativeHours = [int for int in range(-23, 0)]
    return int(positiveHours[negativeHours.index(integer)])


class AqStatist:
    '''
    Класс для работы со статистикой значений датчиков (статистический
    агент).
    Позволяет записывать значение в CSV-файл статистики и получать 
    статистику различными способами.

    Статистика хранится в папке '{папка расположения AsQamm}/statistic'
    в виде СSV-таблиц. Это позволяет эффективно расходовать место на диске.

    Мониторы датчиков через каждый заданный период времени регистрируют
    их значение в архиве через этот класс.
    '''
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

    def __init__(self):
        '''
        Инициализировать статистический агент; коструктор не принимают
        аргументов
        '''
        #КОСТЫЛЬ: Упрощённое хранение статистики без использования архивов
        self.currentCsvFile = f'statistic/{time.strftime("%d%b%Y")}.asqd'
        self.logger = AqLogger('Server>Statist')
        self.isBusy = bool(False)


    def registerStatistic(self, vtime: datetime.datetime, valueId: str, value) -> None:
        '''
        Записать значение датчика в файл статистики.

        :param 'valueId': str
            Индентификатор датчика, значение которого записывают. Больше
            информации о индентификаторах датчиков можно узнать в докумен-
            тации к AqArduinoSensor.getId()

        :param 'value':
            Значение датчика, которое нужно записать

        :returns: None
        '''
        assert value

        self.isBusy = True
        timer = time.perf_counter_ns()

        #Если дата изменилась, создать новый файл
        if f'statistic/{time.strftime("%d%b%Y")}.asqd' != self.currentCsvFile:
            self.currentCsvFile = f'statistic/{time.strftime("%d%b%Y")}.asqd'
            with open(self.currentCsvFile, 'x', encoding = 'utf-8', newline = '') as csvFile:
                csvFile.write('time,valueId,value\n')

        #Проверить, на месте ли заголовок, если его нет, то добавить
        try:
            with open(self.currentCsvFile, 'r+', encoding = 'utf-8', newline = '') as csvFile:
                fileText = csvFile.read()
                if not fileText.startswith('time,valueId,value\n'): csvFile.write(f'time,valueId,value\n{fileText}')

        except FileNotFoundError:
            with open(self.currentCsvFile, 'x', encoding = 'utf-8', newline = '') as csvFile:
                csvFile.write('time,valueId,value\n')
        
        #Занести значение в конец файла
        with open(self.currentCsvFile, 'a', encoding = 'utf-8', newline = '') as csvFile:
            csvFile.write(
                f'{(vtime.hour if vtime.hour >= 10 else f"0{vtime.hour}")}:'
                f'{vtime.minute if vtime.minute >= 10 else f"0{vtime.minute}"},'
                f'{valueId},{value}\n')

        endtimer = time.perf_counter_ns()
        #self.logger.debug(f'Статистический агент сообщил, что регистрация значения заняла {endtimer - timer} наносекунд.')
        self.isBusy = False
        del timer, endtimer
    
        
    def getStatsByTimeQuery(self, query: str) -> list:
        '''
        Получить статистику по выборке времени в виде списка словарей
        по следующему образцу:

        [
            /*Каждый словарь представляет собой набор значений датчиков
              для конкретного времени:
              a —— Время в формате "HH:MM";
              b —— Индентификатор датчика, значение которого записано;
              c —— Значение датчика
            */
            {
                "time": a,
                b: c,
                
                //Другие пары "ID датчика": значение
            }
        ]

        :param 'query': str
            Выборка с определённым синтаксисом. Шпаргалка
            по этому методу в виде изображения — 'Docs_getStatsByTimeQuery.png'
        '''
        Query, Stats, capables, lockedArgs = [], [], [], []


        #Если выборка состоит из 1 аргумента и не имеет уточнения оборудования
        if len(query) == 5:
            print(201)
            Query.append(query[:-2])
            print(Query)
            if Query[0].endswith('Y'):
                maxYear = int(time.strftime('%Y'))
                minYear = maxYear - int((Query[0])[:-1])

                for fily in glob.glob('statistic/*.asqd'):
                    if int((fily.replace('\\', '/'))[15:-5]) in range(minYear, maxYear):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue


            elif Query[0].endswith('M'):
                maxMonth = int(time.strftime('%m'))
                minMonth = maxMonth - int((Query[0])[:-1])
                if minMonth <= 0: minMonth = reverseMonths(minMonth)

                for fily in glob.glob('statistic/*.asqd'):
                    if evalMonths((fily.replace('\\', '/'))[12:-9]) in range(minMonth, maxMonth):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue


            elif Query[0].endswith('D'):
                maxDay = int(time.strftime('%d')) + 1
                minDay = maxDay - int((Query[1])[:-1])
                if minDay <= 0: minDay = reverseDays(minDay)
                
                for fily in glob.glob('statistic/*.asqd'):
                    if int((fily.replace('\\', '/'))[10:-12]) in range(minDay, maxDay):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue
                    

            elif Query[0].endswith('H'):
                maxHour = int(time.strftime('%H')) + 1
                minHour = maxHour - int((Query[1])[:-1])
                if minHour < 0: minHour = reverseHours(minHour)

                if minHour > int(time.strftime('%H')):
                    with open(f'statistic/{int(time.strftime("%d")) - 1}{time.strftime("%b%Y")}', 'r') as statisticFile:
                        for statisticItem in json.loads(statisticFile.read()):
                            if int((statisticItem['time'])[:-3]) >= minHour:
                                Stats.append(statisticItem)

                    with open(self.currentCsvFile, 'r') as statisticFile:
                        for statisticItem in json.loads(statisticFile.read()):
                            if int((statisticItem['time'])[:-3]) in range(minHour, maxHour):
                                Stats.append(statisticItem)

                else:
                     with open(self.currentCsvFile, 'r') as statisticFile:
                        for statisticItem in json.loads(statisticFile.read()):
                            if int((statisticItem['time'])[:-3]) in range(minHour, maxHour):
                                Stats.append(statisticItem)


        #Если выборка состоит из 2 аргументов, но без уточнения оборудования
        elif len(query) == 8:
            #Часть выборки 1
            Query.append(query[:-5])
            if Query[0].endswith('Y'):
                lockedArgs.append('Y')
                maxYear = int(time.strftime('%Y'))
                minYear = maxYear - int((Query[0])[:-1])

                for fily in glob.glob('statistic/*.asqd'):
                    if int((fily.replace('\\', '/'))[15:-5]) in range(minYear, maxYear):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue


            elif Query[0].endswith('M'):
                lockedArgs.extend(['M', 'Y'])
                maxMonth = int(time.strftime('%m'))
                minMonth = maxMonth - int((Query[0])[:-1])
                if minMonth <= 0: minMonth = reverseMonths(minMonth)

                for fily in glob.glob('statistic/*.asqd'):
                    if evalMonths((fily.replace('\\', '/'))[12:-9]) in range(minMonth, maxMonth):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue


            elif Query[0].endswith('D'):
                lockedArgs.extend(['M', 'Y', 'D'])
                maxDay = int(time.strftime('%d')) + 1
                minDay = maxDay - int((Query[1])[:-1])
                if minDay <= 0: minDay = reverseDays(minDay)
                
                for fily in glob.glob('statistic/*.asqd'):
                    if int((fily.replace('\\', '/'))[10:-12]) in range(minDay, maxDay):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue

            #Часть выборки 2
            Query.append(query[3:-2])
            if Query[1].endswith('M') and ('M' not in lockedArgs):
                maxMonth = int(time.strftime('%m')) + 1
                minMonth = maxMonth - int((Query[1])[:-1])
                
                for fily in capables[:]:
                    if evalMonths(fily[12:-9]) not in range(minMonth, maxMonth):
                        capables.remove(fily)
                    else:
                        continue


            elif Query[1].endswith('D') and ('D' not in lockedArgs):
                maxDay = int(time.strftime('%d')) + 1
                minDay = maxDay - int((Query[1])[:-1])
                if minDay <= 0: minDay = reverseDays(minDay)
                
                for fily in capables[:]:
                    if int(fily[10:-12]) not in range(minDay, maxDay):
                        capables.remove(fily)
                    else:
                        continue


            elif Query[1].endswith('H') and ('H' not in lockedArgs):
                maxHour = int(time.strftime('%H')) + 1
                minHour = maxHour - int((Query[1])[:-1])
                if minHour < 0: minHour = reverseHours(minHour)

                for fily in capables[:]:
                    with open(fily, 'r') as filey:
                        for statisticItem in json.loads(filey.read()):
                            if int((statisticItem['time'])[:-3]) in range(minHour, maxHour):
                                Stats.append(statisticItem)


            elif (Query[1])[2:] in lockedArgs:
                raise libs.exceptions.DuplicateQueryArgumentsException()


        #Если выборка состоит из одного аргумента и определения оборудования
        elif query[3:5] not in '1234567890' and query[5:6] not in 'HDMY' and not query.endswith('()'):
            Query.append(query[:3])
            if Query[0].endswith('Y'):
                maxYear = int(time.strftime('%Y'))
                minYear = maxYear - int((Query[0])[:-1])

                for fily in glob.glob('statistic/*.asqd'):
                    if int((fily.replace('\\', '/'))[15:-5]) in range(minYear, maxYear):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue


            elif Query[0].endswith('M'):
                maxMonth = int(time.strftime('%m'))
                minMonth = maxMonth - int((Query[0])[:-1])
                if minMonth <= 0: minMonth = reverseMonths(minMonth)
                if minMonth > maxMonth: minMonth, maxMonth = maxMonth, minMonth

                for fily in glob.glob('statistic/*.asqd'):
                    if evalMonths((fily.replace('\\', '/'))[12:-9]) in range(minMonth, maxMonth):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue


            elif Query[0].endswith('D'):
                maxDay = int(time.strftime('%d')) + 1
                minDay = maxDay - int((Query[0])[:-1])
                if minDay <= 0: minDay = reverseDays(minDay)
                if minDay > maxDay: minDay, maxDay = maxDay, minDay
                
                for fily in glob.glob('statistic/*.asqd'):
                    if int((fily.replace('\\', '/'))[10:-12]) in range(minDay, maxDay):
                        capables.append(fily.replace('\\', '/'))
                    else:
                        continue
                    

            elif Query[0].endswith('H'):
                maxHour = int(time.strftime('%H')) + 1
                minHour = maxHour - int((Query[0])[:-1]) - 1
                if minHour < 0: minHour = reverseHours(minHour)
                if minHour > maxHour: minHour, maxHour = maxHour. minHour

                if minHour > int(time.strftime('%H')):
                    with open(f'statistic/{int(time.strftime("%d")) - 1}{time.strftime("%b%Y")}', 'r') as statisticFile:
                        for statisticItem in json.loads((pandas.read_csv(statisticFile)).to_json(orient = 'records')):
                            if int((statisticItem['time'])[:-3]) in range(minHour, maxHour) and int(statisticItem['time'][3:]) in range(
                            int(time.strftime('%M'))): Stats.append(statisticItem)

                    with open(self.currentCsvFile, 'r') as statisticFile:
                        for statisticItem in json.loads((pandas.read_csv(statisticFile)).to_json(orient = 'records')):
                            if int((statisticItem['time'])[:-3]) in range(minHour, maxHour) and int(statisticItem['time'][3:]) in range(
                            int(time.strftime('%M'))): Stats.append(statisticItem)

                else:
                     with open(self.currentCsvFile, 'r') as statisticFile:
                        for statisticItem in json.loads((pandas.read_csv(statisticFile)).to_json(orient = 'records')):
                            if int((statisticItem['time'])[:-3]) in range(minHour, maxHour) and int(statisticItem['time'][3:]) in range(
                            int(time.strftime('%M'))): Stats.append(statisticItem)

                for statisticItem in Stats[:]:
                    if (int(statisticItem['time'][:-3]) == minHour
                        and int(statisticItem['time'][3:]) not in range(int(time.strftime('%M')), 59)): Stats.remove(statisticItem)

        #Часть выборки с определением оборудования
        Query.append((query[4:-1]).split(', '))
        print(Query)
        if Stats:
            for statisticItem in Stats[:]:
                newStatisticItem = {'time': statisticItem['time']}
                if Query[1]:
                    for hardwareDefn in Query[1]:
                        if hardwareDefn not in statisticItem.keys(): continue
                        else:
                           newStatisticItem.update({hardwareDefn: statisticItem[hardwareDefn]})
                    Stats.remove(statisticItem)
                    Stats.append(newStatisticItem)
                else: pass


        elif capables:
            for filey in capables:
                newStatisticItem = {}
                if Query[1]:
                    for hardwareDefn in Query[1]:
                        with open(filey, 'r') as statisticFile:
                            for item in json.loads((pandas.read_csv(statisticFile)).to_json(orient = 'records')):
                                newStatisticItem.update({'time': item['time']})
                                if hardwareDefn not in item.keys(): continue
                                else: newStatisticItem.update({hardwareDefn: item[hardwareDefn]})

                else:
                    with open(filey, 'r') as statisticFile:
                        for item in json.loads((pandas.read_csv(statisticFile)).to_json(orient = 'records')):
                            newStatisticItem.update(item)
            Stats.append(newStatisticItem)
        return Stats
