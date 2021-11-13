from PyQt5                             import QtCore, QtGui, QtWidgets
from PyQt5.QtCore                      import *
from PyQt5.QtGui                       import *
from PyQt5.QtWidgets                   import *
from playsound                         import *

import os, time, math, glob, json
import base64, subprocess, hashlib
import logging, traceback, platform
import uibld.mdiTemplates

from colorama import Fore as Fore, Style as Style, init as initColorama
initColorama()


class AqUIFunctions:
    class InfoMessageboxLevel:       pass
    class WarningMessageboxLevel:    pass
    class CriticalMessageboxLevel:   pass


    def showMessageBox(self, root: QtCore.QObject, level: (InfoMessageboxLevel or
                                                     WarningMessageboxLevel or
                                                     CriticalMessageboxLevel), title: str, message: str):

        if   level == self.InfoMessageboxLevel: QtWidgets.QMessageBox.information(root, title, message)
        elif level == self.WarningMessageboxLevel: QtWidgets.QMessageBox.warning(root, title, message)
        elif level == self.CriticalMessageboxLevel: QtWidgets.QMessageBox.critical(root, title, message)


    @staticmethod
    def createLabelsAtMainMenu(root):
        root.ui.hintsSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)


        root.ui.lbl_MenuHint1 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint1.setText('Наш дом')
        root.ui.lbl_MenuHint1.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn1.addWidget(root.ui.lbl_MenuHint1)
        root.ui.lbl_MenuHint1.hide()


        root.ui.lbl_MenuHint2 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint2.setText('Защита')
        root.ui.lbl_MenuHint2.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn2.addWidget(root.ui.lbl_MenuHint2)
        root.ui.lbl_MenuHint2.hide()


        root.ui.lbl_MenuHint3 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint3.setText('Растения')
        root.ui.lbl_MenuHint3.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn3.addWidget(root.ui.lbl_MenuHint3)
        root.ui.lbl_MenuHint3.hide()
        

        root.ui.lbl_MenuHint4 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint4.setText('Оборудование')
        root.ui.lbl_MenuHint4.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn4.addWidget(root.ui.lbl_MenuHint4)
        root.ui.lbl_MenuHint4.hide()
              
        
        root.ui.lbl_MenuHint5 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint5.setText('Конфигурация')
        root.ui.lbl_MenuHint5.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn5.addWidget(root.ui.lbl_MenuHint5)
        root.ui.lbl_MenuHint5.hide()

        
    @staticmethod
    def changeInterfaceMode(self, root, userscore):
        if root.ui.stack.currentWidget() == root.ui.page_Home: root.ui.mda_HomeScreenWidgets.tileSubWindows()

        if ((root.ui.stack.currentWidget()) == (root.ui.page_Plants)) or ((root.ui.stack.currentWidget()) == (root.ui.page_6)):

            if userscore.getCurrentUser().getPermits('pxPlants') == True:

                if root.ui.stack.currentWidget() == (root.ui.page_Plants):
                    root.ui.stack.setCurrentWidget(root.ui.page_6)
                elif root.ui.stack.currentWidget() == (root.ui.page_6):
                    root.ui.stack.setCurrentWidget(root.ui.page_Plants)
            else:
                root.msg = QMessageBox.critical(root, 'Действие запрещено', 'Вы не имеете права на осуществление этого действия')


    # Функция toggleSimpleWidgetInteraction может быть использована для анимирования виджетов простой
    # линейной анимацией. Ей необходимо иметь следующие аргументы: желаемый максимальный размер
    # виджета (ширина/высота в зависимости от типа анимации) и ID виджета, с которым она будет
    # работать.
    
    @staticmethod
    def toggleSimpleWidgetInteraction(root, maxLength, widgetId):
        maxExtend = int()

        if widgetId == 0:
            pass

        elif widgetId == 1: # проверяем аргумент на 1 вариант

            # получаем ширину фрейма 
            width = root.ui.frame_left_menu.width()
            maxExtend = maxLength
            standard = 60

            # установим максимальное значение ширины фрейма
            if width == 60:
                lengthExtended = maxExtend
                root.ui.lbl_MenuHint1.show()
                root.ui.lbl_MenuHint2.show()
                root.ui.lbl_MenuHint3.show()
                root.ui.lbl_MenuHint4.show()
                root.ui.lbl_MenuHint5.show()

            else:
                lengthExtended = standard
                root.ui.lbl_MenuHint1.hide()
                root.ui.lbl_MenuHint2.hide()
                root.ui.lbl_MenuHint3.hide()
                root.ui.lbl_MenuHint4.hide()
                root.ui.lbl_MenuHint5.hide()

            # выполним горизонтальную анимацию
            root.animation1 = QPropertyAnimation(root.ui.frame_left_menu, b"minimumWidth")
            root.animation1.setDuration(200)
            root.animation1.setStartValue(width)
            root.animation1.setEndValue(lengthExtended)
            root.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            root.animation1.start()

            root.animation2 = QPropertyAnimation(root.ui.frame_top_menus, b"minimumWidth")
            root.animation2.setDuration(200)
            root.animation2.setStartValue(width)
            root.animation2.setEndValue(lengthExtended)
            root.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            root.animation2.start() 

            
        elif widgetId == 2: # проверяем второй вариант
            height = root.ui.tbw_DefnCamList.height()
            maxExtend == maxLength
            standard = 64

            # установим максимальное значение высоты фрейма и скроем/отобразим мешающие
            # элементы
            if height == 64:

                root.ui.lbl_DefnCurrSetCamId.hide()
                root.ui.lbl_ReadOnly10.hide()
                root.ui.gvf_DefnCamView.hide()

            else:

                root.ui.lbl_DefnCurrSetCamId.show()
                root.ui.lbl_ReadOnly10.show()
                root.ui.gvf_DefnCamView.show()


    @staticmethod
    def selectPage(id: int, root) -> None:
        if id == 0:
            root.ui.stack.setCurrentWidget(root.ui.page_Home)
            root.ui.lbl_PageName.setText('Наш дом')

        elif id == 1:
            root.ui.stack.setCurrentWidget(root.ui.page_Defense)
            root.ui.lbl_PageName.setText('Защита')

        elif id == 2:
            root.ui.stack.setCurrentWidget(root.ui.page_Plants)
            root.ui.lbl_PageName.setText('Растения')

        elif id == 3:
            root.ui.stack.setCurrentWidget(root.ui.page_Hardware)
            root.ui.lbl_PageName.setText('Оборудование')

        elif id == 4:
            root.ui.stack.setCurrentWidget(root.ui.page_Settings)
            root.ui.lbl_PageName.setText('Конфигурация')

            
    @staticmethod
    def setPopupsOpacity(root):
        root.popupOpacity = float()
        root.popupOpacity = (root.ui.sld_WindowsOpacitySct.value() * 0.0101)

        for item in root.popups:
            item.setWindowOpacity(root.popupOpacity)

            
    @staticmethod
    def generateLoadingAnimation(root):
        print(198)
        root.animation3 = QMovie(':/<resource root>/loading.gif', parent = root)
        root.ui.lbl_LoadingAnimation.setMovie(root.animation3)

        
    @staticmethod
    def showLoadingAnimation(root):
        if not root.ui.frame_left_menu.isVisible(): 
            root.ui.lbl_LoadingAnimation.setGeometry(QtCore.QRect(385, 50, 200, 200))
            root.ui.lbl_LoadingText.setGeometry(QtCore.QRect(360, 260, 250, 25))
        else:
            root.ui.lbl_LoadingAnimation.setGeometry(QtCore.QRect(360, 50, 200, 200))
            root.ui.lbl_LoadingText.setGeometry(QtCore.QRect(335, 260, 250, 25))
            root.ui.frame_top.hide()

        root.ui.stack.setCurrentWidget(root.ui.page_Loading)
        root.animation3.start()

        
    @staticmethod
    def hideLoadingAnimation(root, switchTo: QWidget):
        if not root.ui.frame_top.isVisible() and switchTo != root.ui.page_Login:
            root.ui.frame_top.show()
        else:
            root.ui.frame_top.hide()

        root.animation3.stop()
        root.ui.stack.setCurrentWidget(switchTo)

        
    @staticmethod
    def getDefaultThemeId():
        with open('data/config/~!default!~.asqd', 'r', encoding = 'utf-8') as configFile:
            jsonString = json.loads(str(configFile.read()))
            return jsonString['theme']


    @staticmethod
    def mapThemes(root):
        root.ui.cbb_Theme.clear()
        themes = []
        la = glob.glob('ui/themesheets/*.asqd')
        for file in la:
            with open(file, 'r', encoding = 'utf-8') as themeSheet:
                fileString = themeSheet.read()
                jsonString = json.loads(fileString)
                themes.append(jsonString['themeDesc'])
                continue
        root.ui.cbb_Theme.addItems(themes)

        
    @staticmethod
    def getSelectedThemeId(input):
        text = str()
        for file in glob.glob('ui/themesheets/*.asqd'):
            with open(file, 'r', encoding = 'utf-8') as themeSheet:
                fileString = themeSheet.read()
                jsonString = json.loads(fileString)
                if jsonString['themeDesc'] == input.currentText():
                    text = file[15:-5]
                    break
                else:
                    continue
        if text != None or text != '':
            return text
        else:
            return None

        
    @staticmethod
    def loadSpecifiedTheme(root, themeId: str):
            with open(f'ui/themesheets/{themeId}.asqd', 'r', encoding = 'utf-8') as themeSheet:
                fileString = themeSheet.read()
                jsonString = json.loads(fileString)

                styleSheets = {}
                for key, value in (jsonString['styleSheets']).items():
                    styleSheets.update( {key: str((bytes.fromhex(value)).decode('utf-8'))} )

                iconAddresses = jsonString['icons']

                root.setStyleSheet(styleSheets['mainWindow'])
                root.ui.stack.setStyleSheet(styleSheets['stack'])
                root.ui.frame_left_menu.setStyleSheet(styleSheets['mainMenuFrame'])

                root.ui.btn_HomePage.setStyleSheet(styleSheets['homeScreenMainMenuButton'])
                root.ui.btn_DefensePage.setStyleSheet(styleSheets['defenseScreenMainMenuButton'])
                root.ui.btn_PlantsPage.setStyleSheet(styleSheets['plantsScreenMainMenuButton'])
                root.ui.btn_HardwarePage.setStyleSheet(styleSheets['hardwareScreenMainMenuButton'])
                root.ui.btn_SettingsPage.setStyleSheet(styleSheets['configScreenMainMenuButton'])

                root.ui.frame_top.setStyleSheet(styleSheets['topBarFrame'])
                root.ui.lbl_PageName.setStyleSheet(styleSheets['topBarTexts'])
                root.ui.lbl_ReadOnly1.setStyleSheet(styleSheets['topBarTexts'])
                root.ui.lbl_ReadOnly2.setStyleSheet(styleSheets['topBarTexts'])
                root.ui.lbl_HardwareAll.setStyleSheet(styleSheets['topBarTexts'])
                root.ui.lbl_HardwareOnLine.setStyleSheet(styleSheets['topBarTexts'])
                
                root.ui.btn_InterfaceMode.setStyleSheet(styleSheets['topButtons'])
                root.ui.btn_Apply.setStyleSheet(styleSheets['topButtons'])
                root.ui.btn_Save.setStyleSheet(styleSheets['topButtons'])
                root.ui.btn_InterfaceMode.setStyleSheet(styleSheets['topButtons'])

                root.ui.btn_UserInit.setStyleSheet(styleSheets['loginButtons'])
                root.ui.btn_UserInitAsGuest.setStyleSheet(styleSheets['loginButtons'])

                for popup in root.popups:
                    popup.setStyleSheet(styleSheets['popups'])

                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(iconAddresses['menu_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon1.addPixmap(QtGui.QPixmap(":/inactive/inactive/menu_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_Toggle.setIcon(icon1)

                icon2 = QtGui.QIcon()
                icon2.addPixmap(QtGui.QPixmap(iconAddresses['house_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon2.addPixmap(QtGui.QPixmap(":/inactive/inactive/house_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_HomePage.setIcon(icon2)

                icon3 = QtGui.QIcon()
                icon3.addPixmap(QtGui.QPixmap(iconAddresses['defense_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon3.addPixmap(QtGui.QPixmap(":/inactive/inactive/defense_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_DefensePage.setIcon(icon3)

                icon4 = QtGui.QIcon()
                icon4.addPixmap(QtGui.QPixmap(iconAddresses['plants_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon4.addPixmap(QtGui.QPixmap(":/inactive/inactive/plants_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_PlantsPage.setIcon(icon4)

                icon5 = QtGui.QIcon()
                icon5.addPixmap(QtGui.QPixmap(iconAddresses['hardware_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon5.addPixmap(QtGui.QPixmap(":/inactive/inactive/hardware_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_HardwarePage.setIcon(icon5)

                icon6 = QtGui.QIcon()
                icon6.addPixmap(QtGui.QPixmap(iconAddresses['config_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon6.addPixmap(QtGui.QPixmap(":/inactive/inactive/config_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_SettingsPage.setIcon(icon6)

                icon11 = QtGui.QIcon()
                icon11.addPixmap(QtGui.QPixmap(iconAddresses['config_ico_-c']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                root.ui.btn_HardwareConfigUnit.setIcon(icon11)

                icon7 = QtGui.QIcon()
                icon7.addPixmap(QtGui.QPixmap(iconAddresses['interfacemode_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon7.addPixmap(QtGui.QPixmap(":/inactive/inactive/interfacemode_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_InterfaceMode.setIcon(icon7)

                icon8 = QtGui.QIcon()
                icon8.addPixmap(QtGui.QPixmap(iconAddresses['apply_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon8.addPixmap(QtGui.QPixmap(":/inactive/inactive/apply_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_Apply.setIcon(icon8)

                icon12 = QtGui.QIcon()
                icon12.addPixmap(QtGui.QPixmap(iconAddresses['deny_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                root.ui.btn_HardwareDeleteUnit.setIcon(icon12)

                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap(iconAddresses['save_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon9.addPixmap(QtGui.QPixmap(":/inactive/inactive/save_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_Save.setIcon(icon9)

                icon14 = QtGui.QIcon()
                icon14.addPixmap(QtGui.QPixmap(iconAddresses['save_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                root.ui.btn_HardwareToggleUnitStatsRegistry.setIcon(icon14)

                icon10 = QtGui.QIcon()
                icon10.addPixmap(QtGui.QPixmap(iconAddresses['open_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon10.addPixmap(QtGui.QPixmap(":/inactive/inactive/open_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_Load.setIcon(icon10)

                icon13 = QtGui.QIcon()
                icon13.addPixmap(QtGui.QPixmap(iconAddresses['plus_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                root.ui.btn_HardwareAddUnit.setIcon(icon13)
                
                icon15 = QtGui.QIcon()
                icon15.addPixmap(QtGui.QPixmap(iconAddresses['more_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                root.ui.btn_HardwareAdditionalSettings.setIcon(icon15)


    @staticmethod
    def configureHomePageWidget(root, server, widgetDef):
        print(widgetDef)
        hardwareData = server.get('getHardwareData', json)
        unit = [unit for unit in hardwareData if unit['deviceAddress'] == widgetDef['properties']['valueId'].split(':')[0]][0]
        child = [child for address, child in unit['children'].items() if address.split(':') == widgetDef['properties']['valueId'].split(':')[1:-2]][0]
        valueType = [vtype for vtype in child[1]['retrieves'] if vtype['id'] == widgetDef['properties']['valueId'].split(':')[-1]][0]
        probeFrequency = valueType['frequency']

        widget = getattr(
            uibld.mdiTemplates, widgetDef['template'])(root.ui.mda_HomeScreenWidgets,
            widgetDef['name'], widgetDef['properties'], 
            lambda x: server.get('getLastEntry', json, {'content': x}),
            probeFrequency)
        root.widgets.append(widget)
        root.ui.mda_HomeScreenWidgets.addSubWindow(widget)
        widget.show()


class AqThread(QThread):
    started = pyqtSignal()
    changeLoadingLblText = pyqtSignal()
    finished = pyqtSignal()
    
    def __init__(self, root, *args, **kwargs):
        QThread.__init__(self, parent = root)
        self.root = root
        self.loadingLblText = str()
        self.setup(*args, **kwargs)


class AqCrypto:
    '''
    Статический класс для работы с криптографией.
    '''

    @staticmethod
    def decryptContent(string: str) -> str:
        '''
        Преобразовать зашифрованную Base-64 строку в обыкновенную
        строку.

        :param 'string': str
            Зашифрованная Base-64 строка

        :returns: str
            Расшифрованная из Base-64 cтрока
        '''
        return (base64.b64decode(string.encode('utf-8'))).decode('utf-8')

    
    @staticmethod
    def encryptContent(string: str) -> str:
        '''
        Преобразовать обыкновенную строку в зашифрованную строку
        Base-64.

        :param 'string': str
            Обыкновенная cтрока для зашифровки

        :returns: str
            Зашифрованная Base-64 строка
        '''
        return (base64.b64encode(string.encode('utf-8'))).decode('utf-8')

    
    @staticmethod
    def rawContent(string: str) -> str:
        '''
        Неиспользуемый метод
        '''
        return str(r'{0}'.format(string))

    
    @staticmethod
    def getHmta() -> bytes:
        '''
        Получить случайные 32 байта и вернуть их.

        :returns: bytes
        '''
        return os.urandom(32)

    
    @staticmethod
    def getCut(string: str, byteSet: bytes) -> str:
        return (hashlib.pbkdf2_hmac('sha256', string.encode('utf-8'), byteSet, 256256).hex())


sessionLogFilename = f'logs/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammLog.log'


class AqLogger:
    '''
    Класс канала журналирования.

    Журналирование необходимо для отборажения пользователю информацию о 
    текущих действиях сервера, сообщения о предупреждениях и об ошибках.

    Каналов журналирования (или `логгеров`) может быть сколько угодно.
    При этом итоговый журнал всегда сохраняется в ОДИН файл, имя которого
    определяется при запуске самого ПЕРВОГО канала журналирования.
    Каждый из этих каналов имеет своё имя и настраивается по уровню жур-
    налирования (насколько важные сообщения нужно выводить в консоль и
    сохранять в журнал?).

    Любые файлы журналов сохраняются в папке
    '{папка местонаждения программы}/logs'.
    '''
    class LogLevel:
        'Объект для представления уровня журналирования'
        def __init__(self, lm: int):
            self._level = lm


        def __repr__(self):
            repr(self._level)


        def __eq__(self, other):
            if not hasattr(other, '_level'):
                return self._level == other
            else: return self._level == other._level


        def __gt__(self, other):
            if not hasattr(other, '_level'):
                return self._level > other
            else: return self._level > other._level


        def __lt__(self, other):
            if not hasattr(other, '_level'):
                return self._level < other
            else: return self._level < other._level


        def __ge__(self, other):
            if not hasattr(other, '_level'):
                return self._level >= other
            else: return self._level >= other._level


        def __le__(self, other):
            if not hasattr(other, '_level'):
                return self._level <= other
            else: return self._level <= other._level


    #Возможные уровни журналирования:
    DEBUG = LogLevel(logging.DEBUG)       #Уровень ОТЛАДКА (все сообщения, по умолчанию)
    INFO = LogLevel(logging.INFO)         #Уровень ИНФОРМАЦИЯ (важные сообщения)

    WARNING = LogLevel(logging.WARNING)   #Уровень ПРЕДУПРЕЖДЕНИЯ (сообщения важностью
                                          #ПРЕДУПРЕЖДЕНИЕ и выше)

    ERROR = LogLevel(logging.ERROR)       #Уровень ОШИБКИ (только сообщения об ошибках и
                                          #критические сообщения)

    CRITICAL = LogLevel(logging.CRITICAL) #Уровень ТОЛЬКО КРИТИЧЕСКИЕ (только критические
                                          #сообщения)


    def __init__(self, name: str, logLevel: LogLevel = DEBUG,
                                  disableStdPrint: bool = False,
                                  useColorama: (0, 1, 2) = 1):
        '''
        Инициализировать один канал журналирования.

        :param 'name': str
            Имя канала журналирования

        :param 'logLevel': AqLogger.LogLevel = DEBUG
            Необходимый уровень журналирования.

            Возможные уровни журналирования:
             —— DEBUG (все сообщения, по умолчанию);
             —— INFO (важные сообщения);
             —— WARNING (сообщения важностью 
                ПРЕДУПРЕЖДЕНИЕ и выше);
             —— ERROR (только сообщения об ошибках и
                критические сообщения);
             —— CRITICAL (только критические сообщения)

        :param 'disableStdPrint': bool = False
            По умолчанию, сообщения журнала выводятся в консоль.
            Если этот параметр ложен, то вывод в консоль не будет
            производиться

        :param 'useColorama': int = 1
            Использовать ли цветной текст Colorama, и если да, то
            как. Имеются следующие варианты:
            0 —— отключить использование цветного текста;
            1 —— использовать цветной текст для вывода
                 сообщений в консоль;
            2 —— использовать цветной текст для вывода
                 сообщений в консоль и для файла журнала
        '''
        self.name, self.logLevel, self.printDsb, self.useColorama = name, logLevel, disableStdPrint, useColorama
        self.filenames = list()

        self.Logger = logging.getLogger(name)
        self.formatString = ''
        self.getFilename()
        
        self.Logger.setLevel(self.logLevel._level)

        self.handler = logging.FileHandler(rf'{self.filenames[0]}', 'a+', 'utf-8')
        self.Logger.addHandler(self.handler)


    def setLogLevel(self, logLevel: LogLevel):
        '''
        Установить уровень журналирования.

        :param 'logLevel': AqLogger.LogLevel
            Необходимый уровень журналирования.

            Возможные уровни журналирования:
             —— DEBUG (все сообщения, по умолчанию);
             —— INFO (важные сообщения);
             —— WARNING (сообщения важностью 
                ПРЕДУПРЕЖДЕНИЕ и выше);
             —— ERROR (только сообщения об ошибках и
                критические сообщения);
             —— CRITICAL (только критические сообщения)

        :returns: None
        '''
        self.logLevel = logLevel
        self.Logger.setLevel(logLevel._level)


    def getFilename(self):
        '''
        Сгенерировать имя файла для сохранения лога и сохранить его в список
        'self.filenames'. Метод вызывается при инициализации канала журнали-
        рования, но при этом для сохранения логов всегда используется файл с
        именем, которое было получено при инициализации ПЕРВОГО по счёту
        канала.

        :returns: None
        '''
        self.filenames.append(f'logs/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammLog.log')


    def debug(self, message: str):
        '''
        Опубликовать сообщение с уровнем DEBUG (ОТЛАДКА).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))

        self.Logger.debug(message)
        if self.logLevel == self.DEBUG and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}DEBUG{Style.RESET_ALL}]: {message}')
        

    def info(self, message: str):
        '''
        Опубликовать сообщение с уровнем INFO (ИНФОРМАЦИЯ).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))

        self.Logger.info(message)
        if self.logLevel <= self.INFO and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}INFO{Style.RESET_ALL}]: {message}')


    def warning(self, message: str):
        '''
        Опубликовать сообщение с уровнем WARNING (ПРЕДУПРЕЖДЕНИE).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))

        self.Logger.warning(message)
        if self.logLevel <= self.WARNING and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}WARN{Style.RESET_ALL}]: {message}')


    def error(self, message: str):
        '''
        Опубликовать сообщение с уровнем ERROR (ОШИБКА).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))

        self.Logger.error(message)
        if self.logLevel <= self.ERROR and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}ERROR{Style.RESET_ALL}]: {message}')


    def critical(self, message: str):
        '''
        Опубликовать сообщение с уровнем CRITICAL (КРИТИЧЕСКИЙ).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))
        
        self.Logger.critical(message)
        if self.logLevel <= self.CRITICAL and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: {message}')

    def exception(self, _exception: Exception):
        '''
        Опубликовать сообщение о возникновении исключения

        :param '_exception': Exception
            Объект исключения.

        :returns: None
        '''
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: '
              f'Программа аварийно завершила работу из-за исклоючения {type(exception)}:')
        self.Logger.exception(f'Программа аварийно завершила работу из-за исклоючения {type(exception)}:',
                                exc_info = _exception)


    @staticmethod
    def openLogFolder():
        '''
        Открыть папку с файлами журналов.

        :returns: None
        '''
        os.system('explorer logs')


class AqLocalFunctions:
    def __init__(self):
        self.unsaved = []


    def saveReport(self, data: float, dictio: dict):
        dictio.update({time.strftime('%d.%m %H:%M'): data})

        with open('data/report.txt', 'w', encoding = 'utf-8') as report:
            report.write(json.dumps(dictio))


    def apply(self, root, server, usersCore):
        if QApplication.keyboardModifiers() == Qt.AltModifier and QApplication.keyboardModifiers() == Qt.ControlModifier:
            AqConfigSystem.saveDefaultConfig(root, usersCore, AqUIFunctions.getSelectedThemeId(root.ui.cbb_Theme))
        else:
            AqConfigSystem.saveConfig(root, usersCore, AqUIFunctions.getSelectedThemeId(root.ui.cbb_Theme))

        self.saveUnsavedUsers(root, server, usersCore)
        for AqUser in [AqUser for AqUser in usersCore.users if not AqUser.current]:
            usersCore.users.remove(AqUser)

        root.ui.liw_UsersDbList.clear()
        usersCore.loadUsers(root, server, usersCore)


    def saveUnsavedUsers(self, root, server, usersСore):
        self.unsaved = [AqUser for AqUser in usersСore.users if AqUser.edited]
        self.toDeleteList = [AqUser for AqUser in usersСore.users if AqUser.toDelete]
        self.checker = int()
        self.dumpList = []
        self.dumpList2 = []
        print(self.unsaved[0].login)

        root.rootLogger.info('Инициировано сохранение {0} пользователей с изменениями')
        if len(self.unsaved) == 0:
            QMessageBox.information(root, 'Сохранение завершено', 'Конфигурация сохранена')

        for AqUser in self.unsaved:
            self.dumpData = ({ 'id': (AqUser.id), 'description': (AqUser.description),
                              'type': (AqUser.type), 'filepath': (AqUser.filepath),
                              'login': (AqUser.login.value), 'password': (AqUser.password.value), 
                              'avatarAddress': (AqUser.avatarAddress), 'permits': (AqUser.permits.value),
                              'config': (AqUser.config.getDict()) })

            self.dumpList.append(self.dumpData)    
            AqUser.edited = False
            self.checker += 1

        for AqUser in self.toDeleteList:
            self.dumpData = str(AqUser.login)
            self.dumpList2.append(self.dumpData)

        if len(self.dumpList) != 0:
            server.commutatorLogger.debug('Передача информации серверу...')
            merger = []
            integer = int()
            for i in self.dumpList:
                integer += 1
                merger.append(integer)
                continue

            r = server.post('updateUserdata', json, int, self.dumpList)
            if r == 422:
                QMessageBox.critical(root, '422', '422')
            else:
                server.commutatorLogger.debug('Передача информации серверу завершена')


        if len(self.dumpList2) != 0:
            server.commutatorLogger.debug('Передача информации серверу...')
            r = server.delete('delUserAcc', json, self.dumpList2)
            server.commutatorLogger.debug('Передача информации серверу завершена')


        root.rootLogger.info(f'Сохранение {self.checker} пользователей с изменениями успешно завершено')
        QMessageBox.information(root, 'Сохранение завершено', f'Сохранено {self.checker} пользователей!')


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
    def saveDefaultConfig(root, usersCore, themeString):
        currentUser = usersCore.getCurrentUser()

        if (currentUser.getPermits('pxConfigAsAdmin')):
            with open('data/config/~!default!~.asqd', 'w', encoding = 'utf-8') as configFile:
                jsonString = json.dumps(({ 'preset': None, 
                                           'language': (root.ui.cbb_Language.currentIndex()),
                                           'theme': themeString,
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
                                         }}), indent = 8)
                configFile.seek(0)
                configFile.write(jsonString)

        else:
            QMessageBox.critical(root, 'Действие запрещено', 'Вы не имеете права на осуществление этого действия')


    @staticmethod
    def applyConfig(root, server, usersCore):
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

        root.ui.btn_HomePage.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['homeScreen']))))
        root.ui.btn_DefensePage.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['defenseScreen']))))
        root.ui.btn_PlantsPage.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['plantsScreen']))))
        root.ui.btn_HardwarePage.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['hardwareScreen']))))
        root.ui.btn_SettingsPage.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['configScreen']))))
        root.ui.btn_InterfaceMode.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['changeInterfaceMode']))))
        root.ui.btn_Apply.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['applyChanges']))))
        root.ui.btn_Save.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['saveChanges']))))
        root.ui.btn_Load.setShortcut((QKeySequence.fromString(str(currentUser.config.keyBindings['loadChanges']))))

        for widgetDef in currentUser.config.widgets:
            AqUIFunctions.configureHomePageWidget(root, server, widgetDef)

        del currentUser


class AqConfig:
    def __init__(self, configDict):
        self.language = configDict['language']
        self.theme = configDict['theme']
        self.popupOpacity = configDict['popupOpacity']

        self.loggingMode = configDict['loggingMode']
        self.logSavingMode = configDict['logSavingMode']
        self.logSavingDuration = configDict['logSavingDuration']

        self.keyBindings = configDict['keyBindings']
        self.widgets = configDict['widgets']


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


    def setWidgetData(self, widgetsDict):
        self.widgets = widgetsDict


    def getDict(self):
        return {'preset': None,
                'language': (self.language),
                'theme': (self.theme),
                'popupOpacity': (self.popupOpacity),
                'loggingMode': (self.loggingMode),
                'logSavingMode': (self.logSavingMode),
                'logSavingDuration': (self.logSavingDuration),
                'keyBindings': (self.keyBindings),
                'widgets': (self.widgets)}
