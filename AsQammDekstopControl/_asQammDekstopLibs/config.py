from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox
import json, glob


class AqConfigSystem:
    @staticmethod
    def loadDefaultConfig(root):
        jsonString = str()

        with open('data/config/~!default!~.asqd', 'r', encoding = 'utf-8') as configFile:
            jsonString = configFile.read()
            jsonString = json.loads(jsonString)
            defaultConfig = AqConfig(jsonString)
            return defaultConfig


    @staticmethod
    def loadDefaultConfigDict():
        return {'preset': 'default'}


    @staticmethod
    def loadServerConfig():
        with open('data/config/~!serverdata!~.asqd') as configFile:
            fileString = configFile.read()
            jsonString = json.loads(fileString)


    @staticmethod
    def saveConfig(root, usersCore, themeString: str):
        currentUser = usersCore.getCurrentUser()

        currentUser.config.setupByParam('language', root.ui.cbb_Language.currentIndex())
        currentUser.config.setupByParam('theme', themeString)
        currentUser.config.setupByParam('popupOpacity', root.ui.sld_WindowsOpacitySct.value())
        currentUser.config.setupByParam('loggingMode', root.ui.ckb_ToggleLogs.isChecked())
        currentUser.config.setupByParam('logSavingMode', root.ui.ckb_ToggleLogsArch.isChecked())
        currentUser.config.setupByParam('logSavingDuration', root.ui.cbb_LogsArchMode.currentIndex())

        currentUser.config.setKeyBindings({'homeScreen': ((root.ui.keySequenceEdit.keySequence()).toString()),
		                                        'defenseScreen': ((root.ui.keySequenceEdit_2.keySequence()).toString()),
		                                        'plantsScreen': ((root.ui.keySequenceEdit_3.keySequence()).toString()),
		                                        'hardwareScreen': ((root.ui.keySequenceEdit_4.keySequence()).toString()),
		                                        'configScreen': ((root.ui.keySequenceEdit_5.keySequence()).toString()),
		
		                                        'changeInterfaceMode': ((root.ui.keySequenceEdit_6.keySequence()).toString()),
		                                        'applyChanges': ((root.ui.keySequenceEdit_7.keySequence()).toString()),
		                                        'saveChanges': ((root.ui.keySequenceEdit_8.keySequence()).toString()),
		                		                'loadChanges': ((root.ui.keySequenceEdit_9.keySequence()).toString()) })
        currentUser.edited = True
        del currentUser


    @staticmethod
    def saveDefaultConfig(root, usersCore):
        currentUser = usersCore.getCurrentUser()

        if (currentUser.getPermits('pxConfigAsAdmin')):
            with open('data/config/~!default!~.asqd', 'w', encoding = 'utf-8') as configFile:
                jsonString = str(json.dumps(({ 'preset': None, 'language': (root.ui.cbb_Language.currentIndex()),
                                                               'theme': (root.ui.cbb_Theme.currentIndex()),
                                                               'popupOpacity': (root.ui.sld_WindowsOpacitySct.value()),
                                                               'loggingMode': (root.ui.ckb_ToggleLogs.isChecked()),
                                                               'logSavingMode': (root.ui.ckb_ToggleLogsArch.isChecked()),
                                                               'logSavingDuration': (root.ui.cbb_LogsArchMode.currentIndex()),
                                                               'keyBindings': {
                                                                   'homeScreen': ((root.ui.keySequenceEdit.keySequence()).toString()),
		                                                           'defenseScreen': ((root.ui.keySequenceEdit_2.keySequence()).toString()),
		                                                           'plantsScreen': ((root.ui.keySequenceEdit_3.keySequence()).toString()),
		                                                           'hardwareScreen': ((root.ui.keySequenceEdit_4.keySequence()).toString()),
		                                                           'configScreen': ((root.ui.keySequenceEdit_5.keySequence()).toString()),
		
		                                                           'changeInterfaceMode': ((root.ui.keySequenceEdit_6.keySequence()).toString()),
		                                                           'applyChanges': ((root.ui.keySequenceEdit_7.keySequence()).toString()),
		                                                           'saveChanges': ((root.ui.keySequenceEdit_8.keySequence()).toString()),
		                		                                   'loadChanges': ((root.ui.keySequenceEdit_9.keySequence()).toString()) 
                                                                   }
                                                               }), indent = 8))
                configFile.seek(0)
                configFile.write(jsonString)

        else:
            QMessageBox.critical(root, 'Действие запрещено', 'Вы не имеете права на осуществление этого действия')


    @staticmethod
    def applyConfig(root, usersCore):
        currentUser = usersCore.getCurrentUser()

        root.ui.cbb_Language.setCurrentIndex((currentUser.config.language))

        text = str()
        for i in glob.glob('ui/themesheets/*.asqd'):
            with open(i, 'r', encoding = 'utf-8') as themeSheet:
                jsonString = json.loads(themeSheet.read())
                if i[15:-5] == currentUser.config.theme:
                    root.ui.cbb_Theme.setCurrentText(jsonString['themeDesc'])
                else:
                    continue

        root.ui.sld_WindowsOpacitySct.setValue((currentUser.config.popupOpacity))
        root.ui.ckb_ToggleLogs.setChecked((currentUser.config.loggingMode))
        root.ui.ckb_ToggleLogsArch.setChecked((currentUser.config.logSavingMode))
        root.ui.cbb_LogsArchMode.setCurrentIndex((currentUser.config.logSavingDuration))
        
        root.ui.keySequenceEdit.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['homeScreen']))))
        root.ui.keySequenceEdit_2.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['defenseScreen']))))
        root.ui.keySequenceEdit_3.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['plantsScreen']))))
        root.ui.keySequenceEdit_4.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['hardwareScreen']))))
        root.ui.keySequenceEdit_5.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['configScreen']))))
        root.ui.keySequenceEdit_6.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['changeInterfaceMode']))))
        root.ui.keySequenceEdit_7.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['applyChanges']))))
        root.ui.keySequenceEdit_8.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['saveChanges']))))
        root.ui.keySequenceEdit_9.setKeySequence((QKeySequence.fromString(str(currentUser.config.keyBindings['loadChanges']))))

        for popup in root.popups:
            popup.setWindowOpacity((currentUser.config.popupOpacity))

        root.ui.btn_page1.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['homeScreen']))))
        root.ui.btn_page2.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['defenseScreen']))))
        root.ui.btn_page3.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['plantsScreen']))))
        root.ui.btn_page4.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['hardwareScreen']))))
        root.ui.btn_page5.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['configScreen']))))
        root.ui.btn_InterfaceMode.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['changeInterfaceMode']))))
        root.ui.btn_Apply.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['applyChanges']))))
        root.ui.btn_Save.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['saveChanges']))))
        root.ui.btn_Load.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['loadChanges']))))

        del currentUser


class AqConfig(AqConfigSystem):
    def __init__(self, configDict):
        
        self.language = configDict['language']
        self.theme = configDict['theme']
        print(self.theme)
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


    def setupByParam(self, param, value):
        
        if param == 'language':
            self.language = value
        elif param == 'theme':
            self.theme = value
        elif param == 'popupOpacity':
            self.popupOpacity = value

        elif param == 'loggingMode':
            self.loggingMode = value
        elif param == 'logSavingMode':
            self.logSavingMode = value
        elif param == 'logSavingDuration':
            self.logSavingDuration = value


    def setKeyBindings(self, keyBindingsDict):
        self.keyBindings = keyBindingsDict


    def getDict(self):
        return {'preset': None,
                'language': (self.language),
                'theme': (self.theme),
                'popupOpacity': (self.popupOpacity),
                'loggingMode': (self.loggingMode),
                'logSavingMode': (self.logSavingMode),
                'logSavingDuration': (self.logSavingDuration),
                'keyBindings': (self.keyBindings)}
