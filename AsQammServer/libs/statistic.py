import zipfile, glob, json, pandas, time, os
from libs.functions import AqLogger


def evalMonths(str):
    monthsStrings = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthsInts = [int for int in range(1, 13)]
    return int(monthsInts[(monthsStrings.index(str))])


def reverseMonths(integer):
    positiveMonths = [int for int in range(1, 13)]
    negativeMonths = [int for int in range(-11, 1)]
    return int(positiveMonths[negativeMonths.index(integer)])


def reverseDays(integer):
    positiveDays = [int for int in range(1, 32)]
    if ((int(time.strftime('%m')) - 1) == 2):
        negativeDays = [int for int in range(-29, 1)]
    else: negativeDays = [int for int in range (-32, 1)]
    return int(positiveDays[negativeDays.index(integer)])


def reverseHours(integer):
    positiveHours = [int for int in range(1, 24)]
    negativeHours = [int for int in range(-23, 0)]
    return int(positiveHours[negativeHours.index(integer)])


class AqStatist:
    class DiscorrectQueryException(Exception):
        pass

    class DuplicateQueryArgumentsException(Exception):
        pass

    def __init__(self):
        #КОСТЫЛЬ: Упрощённое хранение статистики без использования архивов
        self.currentCsvFile = f'statistic/{time.strftime("%d%b%Y")}.asqd'
        self.logger = AqLogger('Server>Statist')
        self.isBusy = bool(False)


    def registerStatistic(self, sensorIdToRegister: str, valueToRegister):
        assert valueToRegister
        self.isBusy = True
        timer = time.perf_counter()

        if f'statistic/{time.strftime("%d%b%Y")}.asqd' != self.currentCsvFile:
            self.currentCsvFile = f'statistic/{time.strftime("%d%b%Y")}.asqd'
            with open(self.currentCsvFile, 'x', encoding = 'utf-8', newline = '') as csvFile:
                pass

        try:
            with open(self.currentCsvFile, 'r+', encoding = 'utf-8', newline = '') as csvFile:
                try: jsonString = json.loads((pandas.read_csv(csvFile)).to_json(orient = 'records'))
                except (json.JSONDecodeError, pandas.errors.EmptyDataError): jsonString = []
                
        except FileNotFoundError:
            with open(self.currentCsvFile, 'x', encoding = 'utf-8', newline = '') as csvFile:
                jsonString = []

        with open(self.currentCsvFile, 'w+', encoding = 'utf-8', newline = '') as csvFile:
            for dictionary in jsonString:
                try:
                    if   dictionary['time'] == f'{time.strftime("%H:%M")}' and (dictionary[sensorIdToRegister] != valueToRegister or 
                                                                                dictionary[sensorIdToRegister] == valueToRegister):
                        #Если текущая строка — с текущем временем, но значение для данного sensorIdToRegister нет, то
                        #будет вызван KeyError (cм. строку 31)
                        break

                    elif dictionary['time'] != f'{time.strftime("%H:%M")}':
                        #Если текущая строка содержит время, отличное от текущего, то пропустить её
                        continue

                except KeyError:
                    #Если текущая строка — с текущем временем, но значение для данного sensorIdToRegister нет, то
                    #добавляем это значение в dictionary
                    dictionary.update({sensorIdToRegister: valueToRegister})

            else:
                #Если строки с текущим временем не было найдено
                jsonString.append({'time': f'{time.strftime("%H:%M")}', sensorIdToRegister: valueToRegister})

            csvFile.write((pandas.read_json(json.dumps(jsonString), orient = 'records')).to_csv(index = False))

        self.isBusy = False
        endtimer = time.perf_counter()
        self.logger.debug(f'Статистический агент сообщил, что регистрация значения заняла {endtimer / 1000} секунд.')
        del timer, endtimer


    def getQueriedStats(self, query: str):
        Query = []
        Stats = []
        capables = []
        lockedArgs = []


        #Если выборка состоит из 1 аргумента и не имеет уточнения оборудования
        if len(query) == 5:
            Query.append(query[:-2])
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
                raise DuplicateQueryArgumentsException('Двойное упоминание одинаковых аргументов в строке выборки')

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
