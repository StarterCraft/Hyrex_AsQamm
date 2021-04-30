from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from playsound       import *

from uibld.userCreationDlg import Ui_Dlg_CreateNewUserInUserDb
from uibld.userEditDlg     import Ui_Dlg_EditUserInUserDb
from uibld.userSelfEditDlg import Ui_Dlg_EditCurrentUserInUserDb
from uibld.applyChangesDlg import Ui_Dlg_ApplyChanges

from uibld           import *
from libs.resources  import *
from libs.config     import *
from libs.server     import *
from libs.functions  import AqLogger, sessionLogFilename

import sys, os, base64


class AqMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mkdirs()

        self.rootLogger = AqLogger('Core')

        self.popups = []
        self.sounds = {
            'error': 'data/system/sounds/error.mp3',
            'login': 'data/system/sounds/login.mp3', 
            'logOut': 'data/system/sounds/logout.mp3'}
        
        self.getPopups()


    def mkdirs(self):
        neededDirs = ['/logs', '/crashReports', '/data', '/data/personal', '/data/config', '/data/system']
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
        

    def mainloop(self, app: QApplication):
        self.rootLogger.info('Запуск главного цикла приложения')
        self.show()
        sys.exit(app.exec_())
        

from libs           import AqProtectedAttribute
from libs           import STKTOKEN
from libs.users     import *
from libs.functions import AqUIFunctions, AqLocalFunctions, AqThread, AqCrashHandler
from libs.hardware  import AqHardwareSystem
from libs.catch     import AqCrashHandler


if __name__ == '__main__':
    try:
        if 'autosrvas' in sys.argv:
            if sys.argv[3] == (base64.b85encode((STKTOKEN.value.decode('utf-32')
                                                 ).encode('utf-8'))).decode('utf-8'):

                with open('data/config/~!serverdata!~.asqd', 'r') as configFlie:
                    fileString = base64.b64decode(configFlie.read().encode('utf-8')).decode('utf-8')
                    jsonString = json.loads(fileString)
                
                with open('data/config/~!serverdata!~.asqd', 'w') as configFile:
                    if ':' in sys.argv[2]:
                        jsonString['ip'] = f'{(sys.argv[2].split(":"))[0]}'
                        jsonString['port'] = f'{(sys.argv[2].split(":"))[1]}'
                    else: jsonString['ip'] = f'{sys.argv[2]}'
                    configFlie.write(base64.b64encode((json.dumps(jsonString)).encode('utf-8').decode('utf-8')))


        app = QApplication(sys.argv)

        root = AqMainWindow()
        root.rootLogger.info('Запуск ядра')
        AqUIFunctions.loadSpecifiedTheme(root, (AqUIFunctions.getDefaultThemeId()))
        root.rootLogger.debug('Наложение стандартной темы')
        AqUIFunctions.mapThemes(root)

        server = AqServerCommutator(root)
        server.commutatorLogger.info('Коммутатор сервера инициализирован')

        usersCore = AqUsersSystem(root)
        usersCore.userSystemLogger.debug('Cистема пользователей инициализирована')

        localFunc = AqLocalFunctions()
        root.rootLogger.debug('Инициализирована система локальных данных')

        hardwareSystem = AqHardwareSystem(root, server)
        hardwareSystem.logger.debug('Инициализирована система оборудования')

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
        AqUIFunctions.mapThemes(root)
        AqUIFunctions.generateLoadingAnimation(root)

        hardwareSystem.setHardwareListModel(root)
        root.ui.btn_UserInit.clicked.connect( lambda: usersCore.userInit(root, server, usersCore) )
        root.ui.btn_UserInitAsGuest.clicked.connect( lambda: usersCore.guestUserInit(usersCore, root) )
        root.ui.btn_LogOut.clicked.connect( lambda: usersCore.logOutBegin(root, server, usersCore) )
        root.ui.btn_ChangeCurrentUserSrtt.clicked.connect ( lambda: usersCore.callCurrentUserSetupDlg(root, server, usersCore, usersCore.getInstance(root, True)) )
        root.ui.btn_UserDatabaseAddUser.clicked.connect ( lambda: usersCore.callUserCreationDlg(root, server, usersCore) )
        root.ui.btn_UserDatabaseConfigureUser.clicked.connect( lambda: usersCore.callUserSetupDlg(root, server, usersCore, usersCore.getInstance(root, False)) )
        root.ui.btn_UserDatabaseDeleteUser.clicked.connect( lambda: usersCore.callUserDeletionDlg(root, usersCore.getInstance(root, False)) )
        root.ui.liw_UsersDbList.itemSelectionChanged.connect( lambda: usersCore.updateListWidget(root, usersCore) )
        root.ui.sld_WindowsOpacitySct.valueChanged.connect( lambda: AqUIFunctions.setPopupsOpacity(root) )
        root.ui.btn_InterfaceMode.clicked.connect( lambda: AqUIFunctions.changeInterfaceMode(AqUIFunctions, root, usersCore) )
        root.ui.btn_Apply.clicked.connect( lambda: localFunc.apply(root, server, usersCore) )
        root.ui.btn_OpenLogFolder.clicked.connect( lambda: root.rootLogger.openLogFolder() )
        root.ui.cbb_Theme.currentTextChanged.connect( lambda: AqUIFunctions.loadSpecifiedTheme(root, (AqUIFunctions.getSelectedThemeId(root.ui.cbb_Theme))) )
    
        root.rootLogger.debug('Привязка кнопок в интерфейсе приложения завершена успешно')

        usersCore.lockApp(root, usersCore)
        root.mainloop(app)

    except Exception as exception:
        AqCrashHandler().handle(exception, sessionLogFilename)
