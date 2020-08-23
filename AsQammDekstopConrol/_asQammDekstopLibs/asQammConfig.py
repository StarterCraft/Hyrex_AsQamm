import json

class AqConfigSystem:
    def loadDefaultConfig(self, root):
        jsonString = str()

        with open('data/config/~!default!~.asqd', 'r', encoding = 'utf-8') as configFile:
            jsonString = configFile.read()
            jsonString = json.loads(jsonString)
            return AqConfig(jsonString)


    def loadDefaultConfigDict(self, root):
        return { 'preset': 'default' }


class AqConfig(AqConfigSystem):
    def __init__(self, configDict):
        
        self.language = configDict['language']
        self.theme = configDict['theme']
        self.popupOpacity = configDict['popupOpacity']

        self.loggingMode = configDict['loggingMode']
        self.logSavingMode = configDict['logSavingMode']
        self.logSavingDuration = configDict['logSavingDuration']

        self.keyBindings = configDict['keyBindings']


    def setup(self, configDict):
        self.language = configDict['language']
        self.theme = configDict['theme']
        self.popupOpacity = configDict['popupOpacity']

        self.loggingMode = configDict['loggingMode']
        self.logSavingMode = configDict['logSavingMode']
        self.logSavingDuration = configDict['logSavingDuration']


    def setKeyBindings(self, keyBindingsDict):
        self.keyBindings = keyBindingsDict
