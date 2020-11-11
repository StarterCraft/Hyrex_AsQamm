from libs.config import AqConfigSystem
from libs.logging import AqLogger
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json, base64, os, glob, ffmpeg, hashlib, time, math
from playsound import *


class AqUIFunctions():

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
        if ((root.ui.stack.currentWidget()) == (root.ui.page_3)) or ((root.ui.stack.currentWidget()) == (root.ui.page_6)):

            if userscore.getCurrentUser().getPermits('pxPlants') == True:

                if root.ui.stack.currentWidget() == (root.ui.page_3):
                    root.ui.stack.setCurrentWidget(root.ui.page_6)
                elif root.ui.stack.currentWidget() == (root.ui.page_6):
                    root.ui.stack.setCurrentWidget(root.ui.page_3)
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
    def selectSkin(id, root):
        if id == 1:
            root.ui.stack.setCurrentWidget(root.ui.page_1)
            root.ui.lbl_SkinName.setText('Наш дом')

        elif id == 2:
            root.ui.stack.setCurrentWidget(root.ui.page_2)
            root.ui.lbl_SkinName.setText('Защита')

        elif id == 3:
            root.ui.stack.setCurrentWidget(root.ui.page_3)
            root.ui.lbl_SkinName.setText('Растения')

        elif id == 4:
            root.ui.stack.setCurrentWidget(root.ui.page_4)
            root.ui.lbl_SkinName.setText('Оборудование')

        elif id == 5:
            root.ui.stack.setCurrentWidget(root.ui.page_5)
            root.ui.lbl_SkinName.setText('Конфигурация')

            
    @staticmethod
    def setPopupsOpacity(root):
        root.popupOpacity = float()
        root.popupOpacity = (root.ui.sld_WindowsOpacitySct.value() * 0.0101)

        for item in root.popups:
            item.setWindowOpacity(root.popupOpacity)

            
    @staticmethod
    def generateLoadingAnimation(root):
        root.animation3 = QMovie(':/<resource root>/loading.gif', parent = root)
        root.ui.lbl_LoadingAnimation.setMovie(root.animation3)

        
    @staticmethod
    def showLoadingAnimation(root):
        root.ui.stack.setCurrentWidget(root.ui.page_loading)
        root.animation3.start()

        
    @staticmethod
    def hideLoadingAnimation(root, switchTo):
        root.ui.stack.setCurrentWidget(switchTo)
        root.animation3.stop()

        
    @staticmethod
    def getDefaultThemeId():
        with open('data/config/~!default!~.asqd', 'r') as configFile:
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

                root.ui.btn_page1.setStyleSheet(styleSheets['homeScreenMainMenuButton'])
                root.ui.btn_page2.setStyleSheet(styleSheets['defenseScreenMainMenuButton'])
                root.ui.btn_page3.setStyleSheet(styleSheets['plantsScreenMainMenuButton'])
                root.ui.btn_page4.setStyleSheet(styleSheets['hardwareScreenMainMenuButton'])
                root.ui.btn_page5.setStyleSheet(styleSheets['configScreenMainMenuButton'])

                root.ui.frame_top.setStyleSheet(styleSheets['topBarFrame'])
                root.ui.lbl_SkinName.setStyleSheet(styleSheets['topBarTexts'])
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
                root.ui.btn_page1.setIcon(icon2)

                icon3 = QtGui.QIcon()
                icon3.addPixmap(QtGui.QPixmap(iconAddresses['defense_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon3.addPixmap(QtGui.QPixmap(":/inactive/inactive/defense_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_page2.setIcon(icon3)

                icon4 = QtGui.QIcon()
                icon4.addPixmap(QtGui.QPixmap(iconAddresses['plants_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon4.addPixmap(QtGui.QPixmap(":/inactive/inactive/plants_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_page3.setIcon(icon4)

                icon5 = QtGui.QIcon()
                icon5.addPixmap(QtGui.QPixmap(iconAddresses['hardware_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon5.addPixmap(QtGui.QPixmap(":/inactive/inactive/hardware_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_page4.setIcon(icon5)

                icon6 = QtGui.QIcon()
                icon6.addPixmap(QtGui.QPixmap(iconAddresses['config_ico']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                icon6.addPixmap(QtGui.QPixmap(":/inactive/inactive/config_ico_-i_.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
                root.ui.btn_page5.setIcon(icon6)

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


class AqThread(QThread):
    started = pyqtSignal()
    finished = pyqtSignal()

    class AqPasswordChecker:
        pass

    class AqPinTester:
        pass

    def __init__(self, threadType, **kwargs):
        QThread.__init__(self)
        if threadType == self.AqPasswordChecker:
            self.type = self.AqPasswordChecker
            self.text = kwargs['passwordText']
            self.password = kwargs['userPassword']
            self.r = kwargs['bytesObjectsIter']
            self.textLabel = kwargs['loadingScreenText']
            self.exitVar = bool()
        elif threadType == self.AqPinTester:
            self.type = self.AqPinTester
            self.server = kwargs['server']
            self.exitVar = float()


    def run(self):
        if self.type == self.AqPasswordChecker:
            self.started.emit()
            self.textLabel.setText('Ожидание ответа сервера...')
            matches = []
            for i in self.r:
                self.textLabel.setText('Вход...')
                if self.password == AqCrypto.getCut(AqCrypto, self.text, bytes.fromhex(i)):
                    matches.append(True)
                    self.exitVar = True
                    self.finished.emit()
                    self.textLabel.setText('Подготовка интерфейса...')
                    break
                else:
                    matches.append(False)
                    self.textLabel.setText('Подготовка интерфейса...')
                    continue

            if [bool for bool in matches if (bool == True)] == []:
                self.exitVar = False
                self.finished.emit()
            else:
                pass
        elif self.type == self.AqPinTester:
            self.started.emit()
            B = 4275
            R0 = 100000
            while True:
                reading = (self.server.get('pin', json))['0']
                R = 1023.0 / reading - 1.0
                R = R0*R 
                temperature = 1.0/(math.log(R/R0)/B+1/298.15)-167

                self.exitVar = temperature
                print(f't: {temperature} °C')
                self.finished.emit()
                time.sleep(5)
                continue            


class AqCrypto:
    def __init__(self):
        self.cryptoLogger = AqLogger('Crypto')

    def getFileNamesList(self, exportList):
        for i in range(10, 99):
            self.initialFilename = str(r'customuser_' + str(r'{0}').format(i))
            self.initialFilename = self.initialFilename.encode('utf-8')
            self.initialFilename = base64.b64encode(self.initialFilename)
            self.initialFilename = self.initialFilename.decode('utf-8')
            self.initialFilename = self.initialFilename[0:-2]
            self.initialFilename = self.initialFilename.encode('utf-8')
            
            exportList.append(self.initialFilename)

        self.cryptoLogger.debug('Созданы возможные имена файлов профилей пользователей')


    def seekForFiles(self, root, importList, exportList, flag):

        for item in importList:
                self.gotName = glob.glob(str(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8')))))

                if flag:
                    if self.gotName == []:
                        continue
                    else:
                        exportList.append(r'{0}'.format(self.gotName[0]))

                else:
                    if self.gotName != []:
                        continue
                    else:
                        exportList.append(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8'))))


    def decryptContent(self, s):
        return (base64.b64decode(s.encode('utf-8'))).decode('utf-8')


    def encryptContent(self, s):
        return (base64.b64encode(s.encode('utf-8'))).decode('utf-8')


    def rawContent(s):
        return str(r'{0}'.format(s))


    def getHmta(self):
        return os.urandom(32)


    def getCut(self, _str, bytes):
        return (hashlib.pbkdf2_hmac('sha256', _str.encode('utf-8'), bytes, 256256).hex())


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
                              'login': (AqUser.login), 'password': (AqUser.password), 'avatarAddress': (AqUser.avatarAddress),
                              'permits': (AqUser.permits), 'config': (AqUser.config.getDict()) })

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
