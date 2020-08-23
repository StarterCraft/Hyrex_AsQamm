from AsQammDekstop import *
from _asQammDekstopLibs.functions import AqCrypto
from _asQammDekstopUI.userCreationDlg import Ui_Dlg_CreateNewUserInUserDb
from _asQammDekstopUI.userEditDlg import Ui_Dlg_EditUserInUserDb
from _asQammDekstopUI.userSelfEditDlg import Ui_Dlg_EditCurrentUserInUserDb
from _asQammDekstopLibs.config import AqConfigSystem
from playsound import *

import json, os


class AqUsersSystem(AqMainWindow):

    def __init__(self, root):

        self.crypto = AqCrypto()
        self.config = AqConfigSystem()
        self.loggedIn = bool(False)
        self.users = []
        self.sysFileNames = ["data/system/~!guest!~.asqd"]
        self.userSystemLogger = AqLogger('UserSystem')
        self.possibleFileNames = []
        self.availableFileNames = []
       
        self.getPopups(root)


    def getPopups(self, root):
        
        self.creationDlg = QtWidgets.QDialog()
        root.popups.append(self.creationDlg)

        self.editDlg = QtWidgets.QDialog()
        root.popups.append(self.editDlg)

        self.selfEditDlg = QtWidgets.QDialog()
        root.popups.append(self.selfEditDlg)

        self.creationDlgUi = Ui_Dlg_CreateNewUserInUserDb()
        self.creationDlgUi.setupUi(self.creationDlg)

        self.editDlgUi = Ui_Dlg_EditUserInUserDb()
        self.editDlgUi.setupUi(self.editDlg)

        self.selfEditDlgUi = Ui_Dlg_EditCurrentUserInUserDb()
        self.selfEditDlgUi.setupUi(self.selfEditDlg)


    def lockApp(self, root, core):
        
        if not self.loggedIn:
            
            root.ui.lbl_SkinName.setText('Войдите:')
            root.ui.frame_top.hide()
            root.ui.frame_left_menu.hide()
            root.ui.box_Login.setGeometry(QtCore.QRect(360, 130, 280, 130))
            root.ui.lbl_LoginStatus.hide()

            root.ui.btn_Toggle.setEnabled(False)
            root.ui.btn_page1.setEnabled(False)
            root.ui.btn_page2.setEnabled(False)
            root.ui.btn_page3.setEnabled(False)
            root.ui.btn_page4.setEnabled(False)
            root.ui.btn_page5.setEnabled(False)

            root.ui.btn_Apply.setEnabled(False)
            root.ui.btn_Save.setEnabled(False)
            root.ui.btn_Load.setEnabled(False)

            root.ui.lnI_Login.setText('')
            root.ui.lnI_Password.setText('')

            root.ui.stack.setCurrentWidget(root.ui.page_login)

            self.userSystemLogger.Logger.info('Система пользователей успешно подготовила интерфейс приложения' + 
                                             ' для входа пользователя в систему')


        elif self.loggedIn:
            
            self.selector = [User for User in self.users if (User.current == True)]

            root.ui.lbl_SkinName.setText('Наш дом')
            root.ui.lbl_CurrentUserUsername.setText(self.selector[0].login)
            root.ui.lbl_CurrentUserDescription.setText(self.selector[0].description)
            root.ui.gfv_CurrentUserAvatar.setPixmap(self.selector[0].avatar)

            root.ui.frame_top.show()
            root.ui.frame_left_menu.show()
            root.ui.box_Login.setGeometry(QtCore.QRect(310, 120, 280, 130))

            root.ui.btn_Toggle.setEnabled(True)
            root.ui.btn_page1.setEnabled(True)


            if self.selector[0].getPermits('pxDefnBasic'):
                root.ui.btn_page2.setEnabled(True)
            else:
                root.ui.btn_page2.setEnabled(False)

            if self.selector[0].getPermits('pxPlants'):
                root.ui.btn_page3.setEnabled(True)
            else:
                root.ui.btn_page3.setEnabled(False)

            if self.selector[0].getPermits('pxHardware'):
                root.ui.btn_page4.setEnabled(True)
            else:
                root.ui.btn_page4.setEnabled(False)

            if self.selector[0].getPermits('pxConfig'):
                root.ui.btn_page5.setEnabled(True)
            else:
                root.ui.btn_page5.setEnabled(False)

            if self.selector[0].getPermits('pxConfigAsAdmin'):
                root.ui.box_UsersDbEdit.setTitle('Управление пользователями')
                root.ui.liw_UsersDbList.show()
                root.ui.lbl_SelectedUserUsername.show()
                root.ui.lbl_SelectedUserUsername.show()
                root.ui.gfv_SelectedUserAvatar.show()
                root.ui.btn_UserDatabaseAddUser.show()
                root.ui.btn_UserDatabaseConfigureUser.show()
                root.ui.btn_UserDatabaseDeleteUser.show()
            else:
                root.ui.box_UsersDbEdit.setTitle('Здесь пока ничего нет')
                root.ui.liw_UsersDbList.hide()
                root.ui.lbl_SelectedUserUsername.hide()
                root.ui.lbl_SelectedUserUsername.hide()
                root.ui.gfv_SelectedUserAvatar.hide()
                root.ui.btn_UserDatabaseAddUser.hide()
                root.ui.btn_UserDatabaseConfigureUser.hide()
                root.ui.btn_UserDatabaseDeleteUser.hide()

            root.ui.btn_Apply.setEnabled(True)
            root.ui.btn_Save.setEnabled(True)
            root.ui.btn_Load.setEnabled(True)

            root.ui.stack.setCurrentWidget(root.ui.page_1)

            self.userSystemLogger.Logger.info('Система пользователей успешно подготовила интерфейс приложения' +
                                             ' для использования пользователем {0} после успешного входа в систему'.format(str(self.selector[0].
                                                                                                                               login)))


    def loadUsers(self, core, root):

        self.userSystemLogger.Logger.info('Система пользователей начинает выполнение метода инициализации системных экземпляров' +
                                           ' класса пользователя')

        with open(r'%s' % str(self.sysFileNames[0]), 'r') as dataFile:

            fileString = dataFile.readline()
            jsonString = self.crypto.decryptContent(fileString)
            jsonString = json.loads(jsonString)
            self.userSystemLogger.Logger.debug('Прочитан ASQD-файл, получен словарь для создания экземпляра класса пользователя')

            core.guest = User(core, root, (jsonString['id']), (jsonString['description']), (jsonString['type']), str(self.sysFileNames[0]), 
                              (jsonString['avatarAddress']), (jsonString['login']), (jsonString['password']), (jsonString['permits']),
                              (jsonString['config']))
            core.guest.edited = False


        self.userSystemLogger.Logger.info('Система пользователей начинает выполнение метода инициализации добавленных извне экземпляров' +
                                           ' класса пользователя')

        self.crypto.getFileNamesList(self.possibleFileNames)
        self.crypto.seekForFiles(root, self.possibleFileNames, self.availableFileNames, True)

        for item in self.availableFileNames:
            with open(r'%s' % item, 'r') as dataFile:

                fileString = dataFile.readline()
                jsonString = self.crypto.decryptContent(fileString)
                jsonString = json.loads(jsonString)
                self.userSystemLogger.Logger.debug('Прочитан ASQD-файл, получен словарь для создания экземпляра класса пользователя')

                core.instance = User(core, root, (jsonString['id']), (jsonString['description']), (jsonString['type']), (str(item)),  
                              (jsonString['avatarAddress']), (jsonString['login']), (jsonString['password']), (jsonString['permits']),
                              (jsonString['config']))
                core.instance.edited = False
                self.userSystemLogger.Logger.info('Создан экземпляр класса пользователя: ' + str(core.instance))


    def addToUserList(self, root, object, mode):
        if mode == 0:
            self.users.append(object)
            root.ui.liw_UsersDbList.addItems([object.login])
            self.userSystemLogger.Logger.debug('Экземпляр класса пользователя ({0}) был добавлен в лист экземпляров класса пользователя'.format(
                                                str(object)))
        elif mode == 1:
            for User in object:
                root.ui.liw_UsersDbList.addItems([(User.login)])


    def cleanUserList(self):
        self.userSystemLogger.Logger.info('Система пользователей начинает выполнение метода очистки списка экземпляров класса пользователей ' + 
                                          'после успешного входа в систему')

        self.checker = [User for User in self.users if (User.current == False)]
        self.userSystemLogger.Logger.info('Выборка неактивных пользователей составлена')

        for User in self.checker:
            self.users.remove(User)

        try:
            self.userSystemLogger.Logger.info('Система пользователей успешно завершила выполнение очистки списка экземпляров класса пользователей.' + 
                                          ' В списке остаётся только активный пользователь: {0}'.format(str(self.users[0])))
        except IndexError:
            self.userSystemLogger.Logger.info('Система пользователей успешно завершила выполнение очистки списка экземпляров класса пользователей.' + 
                                          ' Список остаётся пустым, так как выполнен выход из системы')

             
    def userInit(self, root, core, login, password):

        self.selector = [User for User in self.users if (User.login == login and User.password == password)]

        try:
            self.selector[0].setAsCurrent(True)
            self.loggedIn = True

            if self.selector[0].getPermits('pxConfigAsAdmin'):
                self.lockApp(root, core)
            else:
                self.cleanUserList()
                self.lockApp(root, core)
            playsound(root.sounds['login'], False)

            self.userSystemLogger.Logger.info('Вход в систему произведён')

        except IndexError:
            root.ui.box_Login.setGeometry(QtCore.QRect(360, 130, 280, 150))
            root.ui.lbl_LoginStatus.show()
            root.ui.lbl_LoginStatus.setStyleSheet('color: red;')
            root.ui.lbl_LoginStatus.setText('Неверный логин или пароль!')
            self.userSystemLogger.Logger.info('Вход в систему не произведён по причине: 0 — неверный логин или пароль')
            playsound(root.sounds['error'], False)


    def guestUserInit(self, core, root):
        self.userSystemLogger.Logger.info('Система пользователей начинает выполнение метода инициализации пользователя Гость')

        core.users[0].setAsCurrent(True)
        
        self.userSystemLogger.Logger.info('У активного экземпляра класса пользователя ' + str(core.users[0]) + ' установлен параметр активности: ' + 
                                          str(core.users[0].current) + ', экземпляр назначен активным пользователем')

        self.loggedIn = True
        self.userSystemLogger.Logger.debug('Система пользователей перешла в состояние: (Вход в систему произведён)')

        self.cleanUserList()

        self.lockApp(root, core)
        self.userSystemLogger.Logger.debug('Система пользователей после входа в систему успешно завершила разблокировку интерфейса приложения')


    def callUserSetupDlg(self, root, core, userToEdit):
        try:
            if (userToEdit.getPermits('pxConfigAsAdmin') and (userToEdit.current)):
                self.callCurrentUserSetupDlg(root, core, userToEdit)
            else:
                self.userSystemLogger.Logger.debug('Инициирован вызов диалога редактирования пользователя {0}'.format(str(userToEdit.login)))

                self.editDlgUi.gfv_EuAvatarPrev.setPixmap(userToEdit.avatar)
                self.editDlgUi.lbl_EuID.setText(str(userToEdit.id))
                self.editDlgUi.lnI_EuLogin.setText(str(userToEdit.login))
                self.editDlgUi.lnI_EuPassword.setText(str(userToEdit.password))
                self.editDlgUi.lnI_EuDesc.setText(str(userToEdit.description))
                self.editDlgUi.lnI_EuAvatarAddr.setText(str(userToEdit.avatarAddress))

                self.editDlgUi.filedialog = QFileDialog()
                self.editDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
                self.editDlgUi.filedialog.fileSelected.connect( lambda: self.editDlgUi.lnI_EuAvatarAddr.setText(str(
                                                                        self.editDlgUi.filedialog.selectedFiles()[0])) )
                self.userSystemLogger.Logger.debug('Инициирован вызов QFileDialog')

                self.editDlgUi.tlb_Browse.clicked.connect( lambda:  self.editDlgUi.filedialog.show() )
                self.editDlgUi.lnI_EuAvatarAddr.textChanged.connect( lambda: self.editDlgUi.gfv_EuAvatarPrev.setPixmap(QPixmap(QImage(str(
                                                                    self.editDlgUi.lnI_EuAvatarAddr.text())))) )

                self.editDlgUi.ckb_UserPermit_HomeRooms.setChecked(userToEdit.getPermits('pxHomeRooms'))
                self.editDlgUi.ckb_UserPermit_HomeAsAdmin.setChecked(userToEdit.getPermits('pxHomeAsAdmin'))
                self.editDlgUi.ckb_UserPermit_DefnScr.setChecked(userToEdit.getPermits('pxDefnBasic'))
                self.editDlgUi.ckb_UserPermit_DefnDbEdit.setChecked(userToEdit.getPermits('pxDefnDbEdit'))
                self.editDlgUi.ckb_UserPermit_DefnAsAdmin.setChecked(userToEdit.getPermits('pxDefnAsAdmin'))
                self.editDlgUi.ckb_UserPermit_PtsScr.setChecked(userToEdit.getPermits('pxPlants'))
                self.editDlgUi.ckb_UserPermit_PtsAsAdmin.setChecked(userToEdit.getPermits('pxPlantsAsAdmin'))
                self.editDlgUi.ckb_UserPermit_HardwareScr.setChecked(userToEdit.getPermits('pxHardware'))
                self.editDlgUi.ckb_UserPermit_HardwareAsAdmin.setChecked(userToEdit.getPermits('pxHardwareAsAdmin'))
                self.editDlgUi.ckb_UserPermit_CfgScr.setChecked(userToEdit.getPermits('pxConfig'))
                self.editDlgUi.ckb_UserPermit_CfgAsAdmin.setChecked(userToEdit.getPermits('pxConfigAsAdmin'))
                                       

                self.editDlg.accepted.connect ( lambda: userToEdit.setup(core, root, (self.editDlgUi.lnI_EuPassword.text()), (self.editDlgUi.lnI_EuDesc.text()),
                                                                        (self.editDlgUi.lnI_EuAvatarAddr.text()),
                                                                        { 'homeRooms': (self.editDlgUi.ckb_UserPermit_HomeRooms.isChecked()),
                                                                          'homeAsAdmin': (self.editDlgUi.ckb_UserPermit_HomeAsAdmin.isChecked()),
                                                                          'defenseBasic': (self.editDlgUi.ckb_UserPermit_DefnScr.isChecked()),
                                                                          'defenseDbEdit': (self.editDlgUi.ckb_UserPermit_DefnDbEdit.isChecked()),
                                                                          'defenseAsAdmin': (self.editDlgUi.ckb_UserPermit_DefnAsAdmin.isChecked()),
                                                                          'plants': (self.editDlgUi.ckb_UserPermit_PtsScr.isChecked()),
                                                                          'plantsAsAdmin': (self.editDlgUi.ckb_UserPermit_PtsScr.isChecked()),
                                                                          'hardware': (self.editDlgUi.ckb_UserPermit_PtsAsAdmin.isChecked()),
                                                                          'hardwareAsAdmin': (self.editDlgUi.ckb_UserPermit_HardwareScr.isChecked()),
                                                                          'configure': (self.editDlgUi.ckb_UserPermit_CfgScr.isChecked()),
                                                                          'configureAsAdmin': (self.editDlgUi.ckb_UserPermit_CfgAsAdmin.isChecked()) } ))

                self.editDlg.show()
                self.userSystemLogger.Logger.debug('Диалог редактирования пользователя {0} открыт'.format(str(userToEdit.login)))

        except AttributeError:
            pass


    def callCurrentUserSetupDlg(self, root, core, userToEdit):
        try:
            self.userSystemLogger.Logger.debug('Инициирован вызов диалога самостоятельного редактирования пользователя {0}'.format(str(userToEdit.login)))

            self.selfEditDlgUi.gfv_EuAvatarPrev.setPixmap(userToEdit.avatar)
            self.selfEditDlgUi.lbl_EuID.setText(str(userToEdit.id))
            self.selfEditDlgUi.lnI_EuLogin.setText(str(userToEdit.login))
            self.selfEditDlgUi.lnI_EuPassword.setText(str(userToEdit.password))
            self.selfEditDlgUi.lnI_EuDesc.setText(str(userToEdit.description))
            self.selfEditDlgUi.lnI_EuAvatarAddr.setText(str(userToEdit.avatarAddress))
            
            self.selfEditDlgUi.filedialog = QFileDialog()
            self.selfEditDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
            self.selfEditDlgUi.filedialog.fileSelected.connect( lambda: self.selfEditDlgUi.lnI_EuAvatarAddr.setText(str(
                                                                    self.selfEditDlgUi.filedialog.selectedFiles()[0])) )
            self.userSystemLogger.Logger.debug('Инициирован вызов QFileDialog')

            self.selfEditDlgUi.tlb_Browse.clicked.connect( lambda:  self.selfEditDlgUi.filedialog.show() )
            self.selfEditDlgUi.lnI_EuAvatarAddr.textChanged.connect( lambda: self.selfEditDlgUi.gfv_EuAvatarPrev.setPixmap(QPixmap(QImage(str(
                                                                self.selfEditDlgUi.lnI_EuAvatarAddr.text())))) )
            
            self.selfEditDlg.accepted.connect ( lambda: userToEdit.setup(core, root, (self.editDlgUi.lnI_EuPassword.text()), (self.editDlgUi.lnI_EuDesc.text()), 
                                                                    (self.editDlgUi.lnI_EuAvatarAddr.text()), (userToEdit.permits)))

            self.selfEditDlg.show()
            self.userSystemLogger.Logger.debug('Диалог редактирования пользователя {0} открыт'.format(str(userToEdit.login)))

        except AttributeError:
            pass


    def callUserDeletionDlg(self, root, userToDelete):
        try:
            self.msg = QMessageBox.question(root, 'Подтверждение действия', 'Вы действительно хотите удалить пользователя %s? Это необратимое действие!' % userToDelete.login)

            if self.msg == QMessageBox.Yes:
                if (userToDelete.type == (0 or '0') or userToDelete.description == 'Guest'):
                    self.msg = QMessageBox.critical(root, 'Действие невозможно', 'Вы не можете удалить системного пользователя!')

                else:
                    try:
                        os.remove((userToDelete.filepath))
                    except FileNotFoundError:
                        pass
                    self.users.remove(userToDelete)
                    root.ui.liw_UsersDbList.clear()
                    self.addToUserList(root, (self.users), 1)
                    self.userSystemLogger.Logger.info('Пользователь %s был удалён' % userToDelete.login)
                    self.msg = QMessageBox.information(root, 'Удаление завершено', 'Пользователь %s был удалён.' % userToDelete.login)

            elif self.msg == QMessageBox.No:
                pass

        except AttributeError:
            pass


    def generateFilenameForNewUser(self, root):
        self.emptyFileNames = []

        self.crypto.seekForFiles(root, self.possibleFileNames, self.emptyFileNames, False)
        return str(self.emptyFileNames[0])


    def callUserCreationDlg(self, root, core):
        try:
            self.creationDlgUi.lbl_CnuID.setText('NaN')
            self.creationDlgUi.lbl_CnuID.setText('')
            self.creationDlgUi.lnI_CnuLogin.setText('')
            self.creationDlgUi.lnI_CnuPassword.setText('')
            self.creationDlgUi.lnI_CnuDesc.setText('')
            self.creationDlgUi.lnI_CnuAvatarAddr.setText('')

            self.creationDlgUi.filedialog = QFileDialog()
            self.creationDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
            self.creationDlgUi.filedialog.fileSelected.connect( lambda: self.creationDlgUi.lnI_CnuAvatarAddr.setText(str(
                                                                self.creationDlgUi.filedialog.selectedFiles()[0])) )

            self.creationDlgUi.tlb_Browse.clicked.connect( lambda:  self.creationDlgUi.filedialog.show() )
            self.creationDlgUi.lnI_CnuAvatarAddr.textChanged.connect ( lambda: self.creationDlgUi.gfv_CnuAvatarPrev.setPixmap(
                                                                               QPixmap(QImage(str(
                                                                               self.creationDlgUi.lnI_CnuAvatarAddr.text())))) )

            self.creationDlg.permits = dict( homeRooms = self.creationDlgUi.ckb_UserPermit_HomeRooms.isChecked(),
                                            homeAsAdmin = self.creationDlgUi.ckb_UserPermit_HomeAsAdmin.isChecked(),
                                            defenseBasic = self.creationDlgUi.ckb_UserPermit_DefnScr.isChecked(),
                                            defenseDbEdit = self.creationDlgUi.ckb_UserPermit_DefnDbEdit.isChecked(),
                                            defenseAsAdmin = self.creationDlgUi.ckb_UserPermit_DefnAsAdmin.isChecked(),
                                            plants = self.creationDlgUi.ckb_UserPermit_PtsScr.isChecked(),
                                            plantsAsAdmin = self.creationDlgUi.ckb_UserPermit_PtsAsAdmin.isChecked(),
                                            hardware = self.creationDlgUi.ckb_UserPermit_HardwareScr.isChecked(), 
                                            hardwareAsAdmin = self.creationDlgUi.ckb_UserPermit_HardwareAsAdmin.isChecked(),
                                            configure = self.creationDlgUi.ckb_UserPermit_CfgScr.isChecked(),
                                            configureAsAdmin = self.creationDlgUi.ckb_UserPermit_CfgAsAdmin.isChecked() )

            self.creationDlg.accepted.connect ( lambda: User(core, root, (self.creationDlgUi.lbl_CnuID.text()), 
                                                             (self.creationDlgUi.lnI_CnuDesc.text()), 1, (self.generateFilenameForNewUser(root)), 
                                                             (self.creationDlgUi.lnI_CnuAvatarAddr.text()), (self.creationDlgUi.lnI_CnuLogin.text()),
                                                             (self.creationDlgUi.lnI_CnuPassword.text()), (self.creationDlg.permits),
                                                             (AqConfigSystem.loadDefaultConfigDict(AqConfigSystem, root))) )

            self.creationDlg.show()

        except AttributeError:
            pass


    def getInstance(self, root, flag):

        if flag:
            self.selector = [User for User in self.users if (User.current)]
            return self.selector[0]
        else:
            try:
                self.selector = [User for User in self.users if ((root.ui.liw_UsersDbList.selectedItems()[0].text()) == User.login)]
                print(self.selector[0])
                return self.selector[0]
            except IndexError:
                self.msg = QMessageBox.warning(root, 'Ошибка', '''Операция невозможна, так как вы не выбрали пользователя из списка.''')
    

    def updateListWidget(self, root, core):
        try:
            self.selector = [User for User in self.users if ((root.ui.liw_UsersDbList.selectedItems()[0].text()) == User.login)]
            root.ui.lbl_SelectedUserUsername.setText(self.selector[0].login)
            root.ui.lbl_SelectedUserDescription.setText(self.selector[0].description)
            root.ui.gfv_SelectedUserAvatar.setPixmap(self.selector[0].avatar)
        except IndexError:
            pass


    def logOut(self, core, root):
        self.userSystemLogger.Logger.info('Инициирован выход из системы.')
        playsound(root.sounds['logOut'], False)

        self.loggedIn = False
        self.userSystemLogger.Logger.debug('Система пользователей перешла в состояние: (Вход в систему не произведён)')

        selector = [User for User in self.users if (User.current == True)]
        selector[0].setAsCurrent(False)
        self.userSystemLogger.Logger.info('У активного экземпляра класса пользователя ' + str(selector[0]) + ' установлен параметр активности: ' + 
                                          str(selector[0].current))

        root.ui.liw_UsersDbList.clear()
        self.userSystemLogger.Logger.info('Очистка списка пользователей')
         
        self.availableFileNames.clear()
        self.possibleFileNames.clear()
        self.cleanUserList()
        self.userSystemLogger.Logger.info('Система пользователей успешно завершила выход из системы')
        self.loadUsers(core, root)
        self.lockApp(root, core)


class User(AqUsersSystem):
    
    def __init__(self, core, root, Id, Desc, Type, Filepath, AvAddr, Login, Password, Permits, ConfigDict):
       
       self.id = Id
       self.type = Type
       self.filepath = Filepath
       self.description = Desc
       self.avatarAddress = AvAddr
       self.avatar = QPixmap((QImage(r'%s' % str(self.avatarAddress))))
       self.login = Login
       self.password = Password
       self.permits = Permits
       self.configDict = ConfigDict
       self.configPreset = ConfigDict['preset']
       
       if self.configPreset != None:
           self.config = core.config.loadDefaultConfig(root)
       else:
           self.config = AqConfig(ConfigDict)

       self.current = bool()
       self.edited = bool(True)

       print(self.filepath)
       core.addToUserList(root, self, 0)


    def setup(self, core, root, Password, Desc, NewAvAddr, Permits):

        self.edited = True
        self.password = Password
        self.description = Desc
        self.avatarAddress = NewAvAddr
        self.permits = Permits
        self.avatar = QPixmap((QImage(r'%s' % str(self.avatarAddress))))
        root.ui.gfv_CurrentUserAvatar.setPixmap(self.avatar)
        root.ui.gfv_SelectedUserAvatar.setPixmap(self.avatar)


    def setAsCurrent(self, bool):
       self.current = bool


    def getPermits(self, permitToKnow):

        if permitToKnow == 'pxHomeRooms':
            return self.permits['homeRooms']
        elif permitToKnow == 'pxHomeAsAdmin':
            return self.permits['homeAsAdmin']

        elif permitToKnow == 'pxDefnBasic':
            return self.permits['defenseBasic']
        elif permitToKnow == 'pxDefnDbEdit':
            return self.permits['defenseDbEdit']
        elif permitToKnow == 'pxDefnAsAdmin':
            return self.permits['defenseAsAdmin']

        elif permitToKnow == 'pxPlants':
            return self.permits['plants']
        elif permitToKnow == 'pxPlantsAsAdmin':
            return self.permits['plantsAsAdmin']

        elif permitToKnow == 'pxHardware':
            return self.permits['hardware']
        elif permitToKnow == 'pxHardwareAsAdmin':
            return self.permits['hardwareAsAdmin']

        elif permitToKnow == 'pxConfig':
            return self.permits['configure']
        elif permitToKnow == 'pxConfigAsAdmin':
            return self.permits['configureAsAdmin']
    