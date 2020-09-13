from _asQammServerLibs.functions import AqCrypto, AqConfig, AqLogger
import json, os

class AqUserSystem():
    def __init__(self):
        self.crypto = AqCrypto()
        self.users = []
        self.userSystemLogger = AqLogger('ServerUserSystem')
        self.possibleFileNames = []
        self.availableFileNames = []
        self.loadUserData()


    def loadUserData(self):

        self.crypto.getFileNamesList(self.possibleFileNames)
        self.crypto.seekForFiles(self.possibleFileNames, self.availableFileNames, True)

        for item in self.availableFileNames:
            with open(r'%s' % item, 'r') as dataFile:

                fileString = dataFile.readline()
                jsonString = self.crypto.decryptContent(fileString)
                jsonString = json.loads(jsonString)

                self.users.append({'id': (int(jsonString['id'])), 'description': (jsonString['description']),
                                  'type': (jsonString['type']), 'filepath': (str(item)), 'login': (jsonString['login']),
                                  'password': (jsonString['password']), 'avatarAddress': (jsonString['avatarAddress']),
                                  'permits': (jsonString['permits']), 'config': (jsonString['config'])})


    def getUserData(self):
        return self.users


    def getUserRegistry(self):
        with open('data/system/~!REG!~.sz', 'r') as dataFile:

            fileString = dataFile.readline()
            jsonString = self.crypto.decryptContent(fileString)
            jsonString = json.loads(jsonString)

            return jsonString
