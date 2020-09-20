from _asQammServerLibs.functions import AqCrypto, AqConfig, AqLogger
from random import choice as randomChoice
import json, os

class AqUserSystem():
    def __init__(self):
        self.crypto = AqCrypto()
        self.users = []
        self.userSystemLogger = AqLogger('Server>UserSystem')
        self.possibleFileNames = []
        self.availableFileNames = []
        self.loadUserData()


    def loadUserData(self):
        self.users.clear()
        self.crypto.getFileNamesList(self.possibleFileNames)
        self.crypto.seekForFiles(self.possibleFileNames, self.availableFileNames, True)

        for item in self.availableFileNames:
            with open(r'%s' % item, 'r') as dataFile:

                fileString = dataFile.readline()
                jsonString = self.crypto.decryptContent(fileString)
                jsonString = json.loads(jsonString)

                self.users.append({'id': (int(jsonString['id'])), 'description': (jsonString['description']),
                                  'type': (jsonString['type']), 'filepath': (item), 'login': (jsonString['login']),
                                  'password': (jsonString['password']), 'avatarAddress': (jsonString['avatarAddress']),
                                  'permits': (jsonString['permits']), 'config': (jsonString['config'])})


    def getUserData(self):
        return self.users


    def getUserRegistry(self):
        with open('data/system/ffreg32.sz', 'r') as dataFile:
            fileString = dataFile.readline()
            jsonString = self.crypto.decryptContent(fileString)
            jsonString = json.loads(jsonString)

            return jsonString


    def updateUserData(self, data: list):
        logins = []
        self.userSystemLogger.debug(data)
        for dict in data:
            with open(dict['filepath'], 'w+') as dataFile:
                fileString = json.dumps(dict)
                fileString = self.crypto.encryptContent(fileString)
                dataFile.write(fileString)
                logins.append(dict['login'])

        self.userSystemLogger.debug('Внесены изменения в аккаунты пользователей {0}'.format(logins))


    def updateUserRegistry(self, data: list):
        with open('data/system/ffreg32.sz', 'w+') as dataFile:
            fileString = json.dumps(data)
            fileString = self.crypto.encryptContent(fileString)
            dataFile.write(fileString)


    def deleteUserAccount(self, data: list):
        logins = []
        for str in data:
            for dict in self.users:
                if str == dict['login']:
                    break
                    os.remove((dict['filepath']))
                else:
                    continue

        self.userSystemLogger.debug('Удалены аккаунты пользователей {0}'.format(logins))


    def getFilenameForNewUser(self):
        self.emptyFileNames = []
        self.crypto.seekForFiles(self.possibleFileNames, self.emptyFileNames, False)
        return str(randomChoice(self.emptyFileNames))
