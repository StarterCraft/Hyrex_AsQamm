from AsQammDekstop import *
import json, base64, os, glob


class AqUIFunctions():

    def createLabelsAtMainMenu(root):

        root.ui.hintsSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        root.ui.styleSheet = str('''QLabel { font: 12pt "Segoe UI Semibold"; color: white; }
        QLabel:hover { color: rgb(47, 105, 23); }''')


        root.ui.lbl_MenuHint1 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint1.setText('Наш дом')
        root.ui.lbl_MenuHint1.setStyleSheet(root.ui.styleSheet)
        root.ui.lbl_MenuHint1.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn1.addWidget(root.ui.lbl_MenuHint1)
        root.ui.lbl_MenuHint1.hide()


        root.ui.lbl_MenuHint2 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint2.setText('Защита')
        root.ui.lbl_MenuHint2.setStyleSheet(root.ui.styleSheet)
        root.ui.lbl_MenuHint2.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn2.addWidget(root.ui.lbl_MenuHint2)
        root.ui.lbl_MenuHint2.hide()


        root.ui.lbl_MenuHint3 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint3.setText('Растения')
        root.ui.lbl_MenuHint3.setStyleSheet(root.ui.styleSheet)
        root.ui.lbl_MenuHint3.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn3.addWidget(root.ui.lbl_MenuHint3)
        root.ui.lbl_MenuHint3.hide()
        

        root.ui.lbl_MenuHint4 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint4.setText('Оборудование')
        root.ui.lbl_MenuHint4.setStyleSheet(root.ui.styleSheet)
        root.ui.lbl_MenuHint4.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn4.addWidget(root.ui.lbl_MenuHint4)
        root.ui.lbl_MenuHint4.hide()
              
        
        root.ui.lbl_MenuHint5 = QtWidgets.QLabel(parent = root.ui.frame_top_menus)
        root.ui.lbl_MenuHint5.setText('Конфигурация')
        root.ui.lbl_MenuHint5.setStyleSheet(root.ui.styleSheet)
        root.ui.lbl_MenuHint5.setSizePolicy(root.ui.hintsSizePolicy)

        root.ui.cel_TopMenuBtn5.addWidget(root.ui.lbl_MenuHint5)
        root.ui.lbl_MenuHint5.hide()


    def changeInterfaceMode(self, root, userscore):
        if (root.ui.stack.currentWidget()) == (root.ui.page_3):
            self.selector = [User for User in userscore.users if (User.current == True)]

            if self.selector[0].permits['plants'] == True:
                root.ui.stack.setCurrentWidget(root.ui.page_6)
            else:
                root.msg = QMessageBox.critical('Действие запрещено', 'Вы не имеете права на осуществление этого действия')


    # Функция toggleSimpleWidgetInteraction может быть использована для анимирования виджетов простой
    # линейной анимацией. Ей необходимо иметь следующие аргументы: желаемый максимальный размер
    # виджета (ширина/высота в зависимости от типа анимации) и ID виджета, с которым она будет
    # работать.

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


    def selectSkin(id, main):

        if id == 1:
            main.ui.stack.setCurrentWidget(main.ui.page_1)
            main.ui.lbl_SkinName.setText('Наш дом')

        elif id == 2:
            main.ui.stack.setCurrentWidget(main.ui.page_2)
            main.ui.lbl_SkinName.setText('Защита')

        elif id == 3:
            main.ui.stack.setCurrentWidget(main.ui.page_3)
            main.ui.lbl_SkinName.setText('Растения')

        elif id == 4:
            main.ui.stack.setCurrentWidget(main.ui.page_4)
            main.ui.lbl_SkinName.setText('Управление')

        elif id == 5:
            main.ui.stack.setCurrentWidget(main.ui.page_5)
            main.ui.lbl_SkinName.setText('Конфигурация')


    def setPopupsOpacity(root):
        root.popupOpacity = float()
        root.popupOpacity = (root.ui.sld_WindowsOpacitySct.value() * 0.0101)

        for item in root.popups:
            item.setWindowOpacity(root.popupOpacity)

        root.rootLogger.Logger.debug('Установлено новое значение popupOpacity: {0}'.format(root.popupOpacity))


class AqCrypto:
    def __init__(self):
        self.cryptoLogger = AqLogger('Crypto')

    def getFileNamesList(self, exportList):

        for i in range(10, 99):
            self.initialFilename = str(r'customuser_' + str(r'{0}').format(i))
            self.initialFilename = self.initialFilename.encode('utf-8')
            self.initialFilename = base64.b64encode(self.initialFilename)
            
            exportList.append(self.initialFilename)

        self.cryptoLogger.Logger.debug('Созданы возможные имена файлов профилей пользователей')


    def seekForFiles(self, importList, exportList, flag):

        for item in importList:
                self.gotName = glob.glob(str(r'data\personal\~!{0}!~.asqd'.format(str(item.decode('utf-8')))))

                if flag:
                    if self.gotName == []:
                        continue
                    else:
                        exportList.append(r'{0}'.format(self.gotName[0]))
                else:
                    if self.gotName != []:
                        continue
                    else:
                        exportList.append(r'data\personal\~!{0}!~.asqd'.format(str(item.decode('utf-8'))))


    def decryptContent(self, str):
        return (base64.b64decode(str.encode('utf-8'))).decode('utf-8')


    def encryptContent(self, str):
        return base64.b64encode(str.encode('uft-8'))

    def rawContent(s):
        return str(r'{0}'.format(s))


class AqLocalFunctions(AqMainWindow):
    def __init__(self):
        self.unsaved = []
        self.saveDialog = None
        self.crypto = AqCrypto()

    def saveUnsaved(self, userscore):
        self.unsaved = [User for User in userscore.users if (User.edited == True)]

        self.possibleFileNames = []
        self.availableFileNames = []
        self.crypto.getFileNamesList(self.possibleFileNames)
        self.crypto.seekForFiles(self.possibleFileNames, self.availableFileNames, False)

        for User in self.unsaved:
            with open((self.availableFileNames[0]), 'a+', encoding = 'utf-8') as dataFile:

                self.dumpData = { 'id': (User.id), 'avatarAddress': (User.avatarAddress)}
                json.dump()
