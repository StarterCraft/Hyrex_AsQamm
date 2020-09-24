import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from playsound import playsound, PlaysoundException

from _asQammDekstopUI.userCreationDlg import Ui_Dlg_CreateNewUserInUserDb
from _asQammDekstopUI.userEditDlg import Ui_Dlg_EditUserInUserDb
from _asQammDekstopUI.userSelfEditDlg import Ui_Dlg_EditCurrentUserInUserDb
from _asQammDekstopUI.applyChangesDlg import Ui_Dlg_ApplyChanges

from _asQammDekstopUI import *
from _asQammDekstopLibs.resources import *
from _asQammDekstopLibs.logging import *
from _asQammDekstopLibs.config import *
from _asQammDekstopLibs.server import *


class AqMainWindow(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mkdirs()

        self.rootLogger = AqLogger('Main')

        self.popups = []
        self.sounds = {
            'error': 'data/system/sounds/error.mp3',
            'login': 'data/system/sounds/login.mp3', 
            'logOut': 'data/system/sounds/logout.mp3'}
        
        self.getPopups()


    def mkdirs(self):
        neededDirs = ['/log', '/data', '/data/personal', '/data/config', '/data/system']
        rootdir = os.getcwd()

        for i in neededDirs:
            try:
                os.makedirs(str(rootdir + i))
            except FileExistsError:
                continue
            
    
    def getPopups(self):
        
        self.applyChangesDlg = QtWidgets.QDialog()
        self.popups.append(self.applyChangesDlg)

        self.userCreationDlg = QtWidgets.QDialog()
        self.popups.append(self.userCreationDlg)

        self.userEditDlg = QtWidgets.QDialog()
        self.popups.append(self.userEditDlg)

        self.userSelfEditDlg = QtWidgets.QDialog()
        self.popups.append(self.userSelfEditDlg)

        self.applyChangesDlgUi = Ui_Dlg_ApplyChanges()
        self.applyChangesDlgUi.setupUi(self.applyChangesDlg)

        self.userCreationDlgUi = Ui_Dlg_CreateNewUserInUserDb()
        self.userCreationDlgUi.setupUi(self.userCreationDlg)

        self.userEditDlgUi = Ui_Dlg_EditUserInUserDb()
        self.userEditDlgUi.setupUi(self.userEditDlg)

        self.userSelfEditDlgUi = Ui_Dlg_EditCurrentUserInUserDb()
        self.userSelfEditDlgUi.setupUi(self.userSelfEditDlg)
        

    def mainloop(self, app):
        self.rootLogger.info('Запуск главного цикла приложения')
        self.show()
        sys.exit(app.exec_())
        

from _asQammDekstopLibs.users import *
from _asQammDekstopLibs.functions import AqUIFunctions, AqLocalFunctions


if __name__ == '__main__':

    app = QApplication(sys.argv)

    root = AqMainWindow()
    root.rootLogger.info('HYREX ASQAMM Pre-aplha 0.-01a Dekstop')

    server = AqServerCommutator(root, AqCrypto)
    server.commutatorLogger.info('Коммутатор сервера инициализирован')

    usersCore = AqUsersSystem(root)
    usersCore.userSystemLogger.debug('Cистема пользователей инициализирована')

    localFunc = AqLocalFunctions()
    root.rootLogger.debug('Инициализирована система локальных данных')

    AqUIFunctions.createLabelsAtMainMenu(root)
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
    

    usersCore.loadUsers(root, server, usersCore)

    root.ui.btn_UserInit.clicked.connect( lambda: usersCore.userInit(root, server, usersCore) )
    root.ui.btn_UserInitAsGuest.clicked.connect( lambda: usersCore.guestUserInit(usersCore, root) )
    root.ui.btn_LogOut.clicked.connect( lambda: usersCore.logOut(root, server, usersCore) )
    root.ui.btn_ChangeCurrentUserSrtt.clicked.connect ( lambda: usersCore.callCurrentUserSetupDlg(root, server, usersCore, usersCore.getInstance(root, True)) )
    root.ui.btn_UserDatabaseAddUser.clicked.connect ( lambda: usersCore.callUserCreationDlg(root, server, usersCore) )
    root.ui.btn_UserDatabaseConfigureUser.clicked.connect( lambda: usersCore.callUserSetupDlg(root, server, usersCore, usersCore.getInstance(root, False)) )
    root.ui.btn_UserDatabaseDeleteUser.clicked.connect( lambda: usersCore.callUserDeletionDlg(root, usersCore.getInstance(root, False)) )
    root.ui.liw_UsersDbList.itemSelectionChanged.connect( lambda: usersCore.updateListWidget(root, usersCore) )
    root.ui.sld_WindowsOpacitySct.valueChanged.connect( lambda: AqUIFunctions.setPopupsOpacity(root) )
    root.ui.btn_InterfaceMode.clicked.connect( lambda: AqUIFunctions.changeInterfaceMode(AqUIFunctions, root, usersCore) )
    root.ui.btn_Apply.clicked.connect( lambda: localFunc.apply(root, server, usersCore) )
    root.ui.btn_OpenLogFolder.clicked.connect( lambda: root.rootLogger.openLogFolder() )
    

    root.rootLogger.info('Привязка кнопок в интерфейсе приложения завершена успешно')

    usersCore.lockApp(root, usersCore)
    root.mainloop(app)
