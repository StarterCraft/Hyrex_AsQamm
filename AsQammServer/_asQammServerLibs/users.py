from _asQammServerLibs.functions import AqCrypto, AqConfig, AqLogger
from random import choice as randomChoice, shuffle as randomShuffle
import json, os

class AqUserSystem():
    def __init__(self):
        self.crypto = AqCrypto()
        self.users = []
        self.userSystemLogger = AqLogger('Server>UserSystem')
        self.possibleFileNames = []
        self.availableFileNames = []
        self.loadUserData() #Сразу после инициализации системы пользователей загружаем их


    def loadUserData(self):
        #Позволяет загрузить пользователей из ASQD-файлов (в виде dict-объекта)

        self.users.clear() #Очистим список пользователей перед подгрузкой
        self.possibleFileNames.clear()
        self.availableFileNames.clear()

        self.crypto.getFileNamesList(self.possibleFileNames) #Выполним маппинг файлов в папке с файлами пользователей
        self.crypto.seekForFiles(self.possibleFileNames, self.availableFileNames, True)
        print(f'self.availableFileNames: {self.availableFileNames}')

        for item in self.availableFileNames: #Для каждого из фалов выполним открытие и выгрузим данные
            with open(r'%s' % item, 'r') as dataFile:

                fileString = dataFile.readline()
                jsonString = self.crypto.decryptContent(fileString)
                jsonString = json.loads(jsonString)

                self.users.append({'id': (int(jsonString['id'])), 'description': (jsonString['description']),
                                  'type': (jsonString['type']), 'filepath': (item), 'login': (jsonString['login']),
                                  'password': (jsonString['password']), 'avatarAddress': (jsonString['avatarAddress']),
                                  'permits': (jsonString['permits']), 'config': (jsonString['config'])})


    def getUserData(self):
        #Позволяет получить список пользователей в виде dict-объектов, загруженный раннее
        return self.users


    def getUserRegistry(self):
        #Позволяет получить регистр пользователей в виде list(str, ...)-объектa
        with open('data/system/~!ffreg!~.asqd', 'r') as dataFile:
            fileString = dataFile.readline()
            jsonString = self.crypto.decryptContent(fileString)
            jsonString = json.loads(jsonString)

            return jsonString


    def updateUserData(self, data: list):
        #Позволяет обновить аккаунты пользователей
        logins = []
        for dict in data:
            try:
                with open((dict['filepath']), 'w+') as dataFile:
                    fileString = json.dumps(dict)
                    fileString = self.crypto.encryptContent(fileString)
                    dataFile.write(fileString)
                    logins.append(dict['login'])
            except OSError:
                with open((dict['filepath'])[1:-1], 'w+') as dataFile:
                    fileString = json.dumps(dict)
                    fileString = self.crypto.encryptContent(fileString)
                    dataFile.write(fileString)
                    logins.append(dict['login'])

        self.userSystemLogger.debug(f'Внесены изменения в аккаунты пользователей {logins}')
        self.loadUserData()


    def updateUserRegistry(self, data: list or str, mode: int):
        #Позволяет обновить регистр пользователей двумя способами: дополнением или перезаписью
        if mode == 0: #Режим дополнения регистра
            print('append mode')
            with open('data/system/~!ffreg!~.asqd', 'r') as dataFile:
                rg = json.loads(self.crypto.decryptContent(dataFile.read()))

            with open('data/system/~!ffreg!~.asqd', 'w+') as dataFile:
                rg.append(data)
                randomShuffle(rg)
                fileString = json.dumps(rg)
                fileString = self.crypto.encryptContent(fileString)
                dataFile.write(fileString)

        elif mode == 1: #Режим перезаписи регистра
            with open('data/system/~!ffreg!~.asqd', 'w+') as dataFile:
                fileString = json.dumps(data)
                fileString = self.crypto.encryptContent(fileString)
                dataFile.write(fileString)


    def deleteUserAccount(self, data: list):
        #Позволяет удалить аккаунт пользователя
        logins = []
        for str in data:
            for dict in self.users:
                if str == dict['login']:
                    logins.append(str)
                    os.remove(dict['filepath'])
                    self.users.remove(dict)
                    break
                else:
                    continue
            continue

        self.loadUserData()
        self.userSystemLogger.debug(f'Удалены аккаунты пользователей {logins}')


    def getFilenameForNewUser(self):
        self.emptyFileNames = []
        self.crypto.seekForFiles(self.possibleFileNames, self.emptyFileNames, False)
        return str(randomChoice(self.emptyFileNames))
