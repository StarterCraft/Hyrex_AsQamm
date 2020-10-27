#КОСТЫЛЬ: Использование чистого JSON вместо CSV, т. к. с последним не получилось.
import _asQammServerLibs.hardware as hwCore, zipfile, glob, json, time, os
from _asQammServerLibs.functions import AqLogger

class AqStatist:
    class DiscorrectQueryException(Exception):
        pass

    def __init__(self):
        #КОСТЫЛЬ: Упрощённое хранение статистики без использования архивов
        self.currentJsonFile = f'statistic/{time.strftime("%d%b%Y")}.asqd'
        self.logger = AqLogger('Server>Statist')
        with open(self.currentJsonFile, 'a+', encoding = 'utf-8') as jsonFile:
            jsonFile.seek(0)
            if not jsonFile.read():
                jsonFile.write('[]')
                jsonFile.seek(0)
            else:
                pass


    def registerStatistic(self, sensorIdToRegister: str, valueToRegister):
        assert valueToRegister
        if f'statistic/{time.strftime("%d%b%Y")}.asqd' != self.currentJsonFile:
            self.currentJsonFile = f'statistic/{time.strftime("%d%b%Y")}.asqd'
            with open(self.currentJsonFile, 'w+', encoding = 'utf-8') as jsonFile:
                jsonFile.write('[]')
        else:
            with open(self.currentJsonFile, 'a+', encoding = 'utf-8') as jsonFile:
                jsonFile.seek(0)
                if not jsonFile.read():
                    jsonFile.write('[]')
                else:
                    pass

        with open(self.currentJsonFile, 'r+', encoding = 'utf-8') as jsonFile:
            jsonString = json.loads(jsonFile.read())

        with open(self.currentJsonFile, 'w+', encoding = 'utf-8') as jsonFile:
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

            jsonFile.write(json.dumps(jsonString))


    def getQueriedStats(self, query: str):
        if query not in '1234567890HDMY' or len(query) > 6:
            raise DiscorrectQueryException
        else:
            Query = query

        if len()
