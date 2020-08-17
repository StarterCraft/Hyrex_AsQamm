import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from playsound import playsound, PlaysoundException

from _asQamm.asQammUI import *
from _asQamm.asQammResources import *
from _asQamm.asQammLogging import *


class AqMainWindow(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mkdirs()

        self.rootLogger = AqLogger('Main')
        self.rootLogger.Logger.info('Инициализация корневого класса')

        self.popups = []


    def mkdirs(self):
        neededDirs = ['/log', '/data', '/data/personal', '/data/config', '/data/system']
        rootdir = os.getcwd()

        for i in neededDirs:
            try:
                os.makedirs(str(rootdir + i))
            except FileExistsError:
                continue


    def mainloop(self, app):
        self.rootLogger.Logger.info('Запуск главного цикла приложения')
        self.show()
        sys.exit(app.exec_())
        

from _asQamm.asQammUsers import *
from _asQamm.asQammFunctions import AqUIFunctions


if __name__ == "__main__":

    app = QApplication(sys.argv)

    root = AqMainWindow()
    root.rootLogger.Logger.info('Экземпляр корневого класса успешно создан: ' + str(root))

    usersCore = AqUsersSystem(root)
    usersCore.userSystemLogger.Logger.debug('Экземпляр класса системы пользователей успешно создан: ' + str(usersCore))

    AqUIFunctions.createLabelsAtMainMenu(root)
    root.rootLogger.Logger.info('Всплывающие подсказки меню успешно сгенерированы! ')

    # Добавляем привязки клавиш к анимациям
    root.ui.btn_Toggle.clicked.connect(lambda: AqUIFunctions.toggleSimpleWidgetInteraction(root, 190, 1))
    root.ui.btn_DefnToggleCamList.toggled.connect(lambda: AqUIFunctions.toggleSimpleWidgetInteraction(root, 320, 2))

    # Cкин Дом
    root.ui.btn_page1.clicked.connect( lambda: AqUIFunctions.selectSkin(1, root) )

    # Скин Защита
    root.ui.btn_page2.clicked.connect( lambda: AqUIFunctions.selectSkin(2, root) )

    # Скин Растения
    root.ui.btn_page3.clicked.connect( lambda: AqUIFunctions.selectSkin(3, root) )

    # Скин Управление
    root.ui.btn_page4.clicked.connect( lambda: AqUIFunctions.selectSkin(4, root) )

    # Скин Конфигурации
    root.ui.btn_page5.clicked.connect( lambda: AqUIFunctions.selectSkin(5, root) )
    

    usersCore.loadUsers(usersCore, root)

    root.ui.btn_UserInit.clicked.connect( lambda: usersCore.userInit(root, usersCore, root.ui.lnI_Login.text(), root.ui.lnI_Password.text()) )
    root.ui.btn_UserInitAsGuest.clicked.connect( lambda: usersCore.guestUserInit(usersCore, root) )
    root.ui.btn_LogOut.clicked.connect( lambda: usersCore.logOut(usersCore, root) )
    root.ui.btn_ChangeCurrentUserSrtt.clicked.connect ( lambda: usersCore.callUserSetupDlg(root, usersCore, usersCore.getInstance(root, True)) )
    root.ui.btn_UserDatabaseAddUser.clicked.connect ( lambda: usersCore.callUserCreationDlg(root, usersCore) )
    root.ui.btn_UserDatabaseConfigureUser.clicked.connect( lambda: usersCore.callUserSetupDlg(root, usersCore, usersCore.getInstance(root, False)) )
    root.ui.btn_UserDatabaseDeleteUser.clicked.connect( lambda: usersCore.callUserDeletionDlg(root, usersCore.getInstance(root, False)) )
    root.ui.liw_UsersDbList.itemSelectionChanged.connect( lambda: usersCore.updateListWidget(root, usersCore) )
    root.ui.sld_WindowsOpacitySct.valueChanged.connect ( lambda: AqUIFunctions.setPopupsOpacity(root) )
    root.ui.btn_InterfaceMode.clicked.connect ( lambda: AqUIFunctions.changeInterfaceMode(root, usersCore) )

    root.rootLogger.Logger.info('Привязка кнопок в интерфейсе приложения завершена успешно')

    usersCore.lockApp(root, usersCore)
    root.mainloop(app)
