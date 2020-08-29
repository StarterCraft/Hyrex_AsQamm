from AsQammDekstop import *
import json, base64, os, glob, ffmpeg
from playsound import *


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
            root.ui.lbl_SkinName.setText('Управление')

        elif id == 5:
            root.ui.stack.setCurrentWidget(root.ui.page_5)
            root.ui.lbl_SkinName.setText('Конфигурация')


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


    def seekForFiles(self, root, importList, exportList, flag):

        for item in importList:
                self.gotName = glob.glob(str(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8')))))

                if flag:
                    if self.gotName == []:
                        continue
                    else:
                        exportList.append(r'{0}'.format(self.gotName[0]))

                    if len(exportList) == 0:
                        QMessageBox.warning(root, 'Ошибка инициализации системы пользователей', '''Не удалось найти ни одного аккаунта
                                            пользователя, за исключением аккаунта гостя. Большая часть функциональности недоступна.
                                            Проверьте, что вы создали хотя бы одного пользователя с правами админинстратора.''')
                    else:
                        pass

                else:
                    if self.gotName != []:
                        continue
                    else:
                        exportList.append(r'data\personal\~!{0}!~.asqd'.format(str(item.decode('utf-8'))))


    def decryptContent(self, str):
        return (base64.b64decode(str.encode('utf-8'))).decode('utf-8')


    def encryptContent(self, str):
        return (base64.b64encode(str.encode('utf-8'))).decode('utf-8')


    def rawContent(s):
        return str(r'{0}'.format(s))


class AqLocalFunctions(AqMainWindow):
    def __init__(self):
        self.unsaved = []


    def apply(self, root, userscore):
        AqConfigSystem.saveConfig(AqConfigSystem, root, userscore)
        self.saveUnsavedUsers(userscore, root)


    def saveUnsavedUsers(self, userscore, root):
        self.unsaved = [AqUser for AqUser in userscore.users if (AqUser.edited == True)]
        self.checker = int()

        for AqUser in self.unsaved:
            with open((AqUser.filepath), mode = 'w+', encoding = 'utf-8') as dataFile:

                self.dumpData = { 'id': (AqUser.id), 'description': (AqUser.description),
                                  'type': (AqUser.type), 'filepath': (AqUser.filepath),
                                  'login': (AqUser.login), 'password': (AqUser.password), 'avatarAddress': (AqUser.avatarAddress),
                                  'permits': (AqUser.permits), 'config': (AqUser.config.getDict()) }

                jsonString = json.dumps((self.dumpData), indent = 8)
                jsonString = AqCrypto.encryptContent(AqCrypto, jsonString)
                dataFile.write(jsonString)
                AqUser.edited = False

                self.checker += 1

        QMessageBox.information(root, 'Операция завершена', 'Сохранено {0} пользователей!'.format((self.checker)))
