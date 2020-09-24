from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from AsQammDekstop import AqMainWindow

from _asQammDekstopLibs.functions import AqCrypto
from _asQammDekstopLibs.config import AqConfigSystem
from _asQammDekstopLibs.logging import AqLogger

from random import choice as randomChoice, shuffle as randomShuffle
from playsound import *

import json, os, requests


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


    def getCurrentUser(self):
        self.selector = [AqUser for AqUser in self.users if (AqUser.current == True)]
        return self.selector[0]
        

    def lockApp(self, root, usersCore):
        
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

            self.userSystemLogger.info('Интерфейс приложения подготовлен для входа пользователя в систему')


        elif self.loggedIn:
            self.currentUser = self.getCurrentUser()

            root.ui.lbl_SkinName.setText('Наш дом')
            root.ui.lbl_CurrentUserUsername.setText(self.currentUser.login)
            root.ui.lbl_CurrentUserDescription.setText(self.currentUser.description)
            root.ui.gfv_CurrentUserAvatar.setPixmap(self.currentUser.avatar)

            root.ui.frame_top.show()
            root.ui.frame_left_menu.show()
            root.ui.box_Login.setGeometry(QtCore.QRect(310, 120, 280, 130))

            root.ui.btn_Toggle.setEnabled(True)
            root.ui.btn_page1.setEnabled(True)

            if self.currentUser.getPermits('pxDefnBasic'):
                root.ui.btn_page2.setEnabled(True)
            else:
                root.ui.btn_page2.setEnabled(False)

            if self.currentUser.getPermits('pxPlants'):
                root.ui.btn_page3.setEnabled(True)
            else:
                root.ui.btn_page3.setEnabled(False)

            if self.currentUser.getPermits('pxHardware'):
                root.ui.btn_page4.setEnabled(True)
            else:
                root.ui.btn_page4.setEnabled(False)

            if self.currentUser.getPermits('pxConfig'):
                root.ui.btn_page5.setEnabled(True)
            else:
                root.ui.btn_page5.setEnabled(False)

            if self.currentUser.getPermits('pxConfigAsAdmin'):
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
            AqConfigSystem.applyConfig(root, usersCore)

            root.ui.stack.setCurrentWidget(root.ui.page_1)

            del self.currentUser


    def loadUsers(self, root, server, usersCore):

        with open(r'%s' % str(self.sysFileNames[0]), 'r') as dataFile:

            fileString = dataFile.readline()
            jsonString = self.crypto.decryptContent(fileString)
            jsonString = json.loads(jsonString)

            usersCore.guest = AqUser(usersCore, root, int(jsonString['id']), (jsonString['description']), (jsonString['type']), str(self.sysFileNames[0]), 
                              (jsonString['avatarAddress']), (jsonString['login']), (jsonString['password']), (jsonString['permits']),
                              (jsonString['config']))
            usersCore.guest.edited = False

        self.userSystemLogger.info('Загрузка аккаунтов пользователей...')
        
        r = server.get('getUserdata', json)
        server.commutatorLogger.info('Подключение к серверу установлено')

        if (len(list(r))) == 0:
            QMessageBox.warning(root, 'Ошибка инициализации системы пользователей', 
                                      '''Не удалось найти ни одного аккаунта пользователя, за исключением аккаунта гостя. Большая часть функциональности недоступна. Проверьте, что вы создали хотя бы одного пользователя с правами админинстратора.''')

        for item in r:
            usersCore.instance = AqUser(usersCore, root, int(item['id']), (item['description']), (item['type']), (item['filepath']),  
                              (item['avatarAddress']), (item['login']), (item['password']), (item['permits']), (item['config']))
            usersCore.instance.edited = False
            self.userSystemLogger.info('Загружен пользователь ' + str(usersCore.instance.login))


    def addToUserList(self, root, object, mode):
        if mode == 0:
            self.users.append(object)
            root.ui.liw_UsersDbList.addItems([object.login])
            
        elif mode == 1:
            for AqUser in object:
                root.ui.liw_UsersDbList.addItems([(AqUser.login)])


    def cleanUserList(self):
        self.checker = [AqUser for AqUser in self.users if (AqUser.current == False)]

        for AqUser in self.checker:
            self.users.remove(AqUser)
           
             
    def userInit(self, root, server, usersCore):

        self.selector = [AqUser for AqUser in self.users if (AqUser.login == root.ui.lnI_Login.text())]
        self.matches = []
        self.userSystemLogger.debug('Инициирован вход в систему как {0}'.format(root.ui.lnI_Login.text()))

        r = server.get('getUserRg', json)
        for i in r:
            try:
                if self.selector[0].password == self.crypto.getCut(root.ui.lnI_Password.text(), bytes.fromhex(i)):
                    self.selector[0].setAsCurrent(True)
                    self.selector[0].edited = False

                    self.loggedIn = True

                    if self.selector[0].getPermits('pxConfigAsAdmin'):
                        self.lockApp(root, usersCore)
                    else:
                        self.cleanUserList()
                        self.lockApp(root, usersCore)
                    
                    playsound(root.sounds['login'], False)
                    self.userSystemLogger.info('Вход в систему произведён пользователем {0}'.format(self.selector[0].login))
                    self.matches.append(True)
                    break
                else:
                    self.matches.append(False)
                    continue

            except IndexError:
                break
                root.ui.box_Login.setGeometry(QtCore.QRect(360, 130, 280, 150))
                root.ui.lbl_LoginStatus.show()
                root.ui.lbl_LoginStatus.setStyleSheet('color: red;')
                root.ui.lbl_LoginStatus.setText('Неверный логин или пароль!')
                self.userSystemLogger.info('Вход в систему не произведён по причине: 0 — неверный логин или пароль')
                playsound(root.sounds['error'], False)
            
        randomShuffle(r)
        server.post('updateUserRg', json, int, [1, r])
        del r

        if [bool for bool in self.matches if (bool == True)] == []:
            root.ui.box_Login.setGeometry(QtCore.QRect(360, 130, 280, 150))
            root.ui.lbl_LoginStatus.show()
            root.ui.lbl_LoginStatus.setStyleSheet('color: red;')
            root.ui.lbl_LoginStatus.setText('Неверный логин или пароль!')
            self.userSystemLogger.info('Вход в систему не произведён по причине: 0 — неверный логин или пароль')
            playsound(root.sounds['error'], False)
        else:
            pass


    def guestUserInit(self, usersCore, root):

        usersCore.users[0].setAsCurrent(True)
        self.userSystemLogger.info('У активного экземпляра класса пользователя ' + str(usersCore.users[0]) + ' установлен параметр активности: ' + 
                                          str(usersCore.users[0].current) + ', экземпляр назначен активным пользователем')

        self.loggedIn = True
        self.cleanUserList()
        self.lockApp(root, usersCore)

        self.userSystemLogger.info('Вход в систему произведён в режиме гостя')


    def callUserSetupDlg(self, root, server, usersCore, userToEdit):
        try:
            if (userToEdit.getPermits('pxConfigAsAdmin') and (userToEdit.current)):
                self.callCurrentUserSetupDlg(root, usersCore, userToEdit)
            else:
                self.userSystemLogger.debug('Инициирован вызов диалога редактирования пользователя {0}'.format(str(userToEdit.login)))

                root.userEditDlgUi.gfv_EuAvatarPrev.setPixmap(userToEdit.avatar)
                root.userEditDlgUi.lbl_EuID.setText(str(userToEdit.id))
                root.userEditDlgUi.lnI_EuLogin.setText(str(userToEdit.login))
                root.userEditDlgUi.lnI_EuDesc.setText(str(userToEdit.description))
                root.userEditDlgUi.lnI_EuAvatarAddr.setText(str(userToEdit.avatarAddress))

                root.userEditDlgUi.filedialog = QFileDialog()
                root.userEditDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
                root.userEditDlgUi.filedialog.fileSelected.connect( lambda: root.userEditDlgUi.lnI_EuAvatarAddr.setText(str(
                                                                        root.userEditDlgUi.filedialog.selectedFiles()[0])) )

                root.userEditDlgUi.tlb_Browse.clicked.connect( lambda:  root.userEditDlgUi.filedialog.show() )
                root.userEditDlgUi.lnI_EuAvatarAddr.textChanged.connect( lambda: root.userEditDlgUi.gfv_EuAvatarPrev.setPixmap(QPixmap(QImage(str(
                                                                    root.userEditDlgUi.lnI_EuAvatarAddr.text())))) )

                root.userEditDlgUi.ckb_UserPermit_HomeRooms.setChecked(userToEdit.getPermits('pxHomeRooms'))
                root.userEditDlgUi.ckb_UserPermit_HomeAsAdmin.setChecked(userToEdit.getPermits('pxHomeAsAdmin'))
                root.userEditDlgUi.ckb_UserPermit_DefnScr.setChecked(userToEdit.getPermits('pxDefnBasic'))
                root.userEditDlgUi.ckb_UserPermit_DefnDbEdit.setChecked(userToEdit.getPermits('pxDefnDbEdit'))
                root.userEditDlgUi.ckb_UserPermit_DefnAsAdmin.setChecked(userToEdit.getPermits('pxDefnAsAdmin'))
                root.userEditDlgUi.ckb_UserPermit_PtsScr.setChecked(userToEdit.getPermits('pxPlants'))
                root.userEditDlgUi.ckb_UserPermit_PtsAsAdmin.setChecked(userToEdit.getPermits('pxPlantsAsAdmin'))
                root.userEditDlgUi.ckb_UserPermit_HardwareScr.setChecked(userToEdit.getPermits('pxHardware'))
                root.userEditDlgUi.ckb_UserPermit_HardwareAsAdmin.setChecked(userToEdit.getPermits('pxHardwareAsAdmin'))
                root.userEditDlgUi.ckb_UserPermit_CfgScr.setChecked(userToEdit.getPermits('pxConfig'))
                root.userEditDlgUi.ckb_UserPermit_CfgAsAdmin.setChecked(userToEdit.getPermits('pxConfigAsAdmin'))
                                       

                root.userEditDlg.accepted.connect ( lambda: userToEdit.setup(usersCore, root, (self.crypto.getCut(root.userSelfEditDlgUi.lnI_EuPassword.text(), bytes.fromhex(randomChoice(server.get('getUserRg', json))))),
                                                                        (root.userEditDlgUi.lnI_EuDesc.text()), (root.userEditDlgUi.lnI_EuAvatarAddr.text()),
                                                                        { 'homeRooms': (root.userEditDlgUi.ckb_UserPermit_HomeRooms.isChecked()),
                                                                          'homeAsAdmin': (root.userEditDlgUi.ckb_UserPermit_HomeAsAdmin.isChecked()),
                                                                          'defenseBasic': (root.userEditDlgUi.ckb_UserPermit_DefnScr.isChecked()),
                                                                          'defenseDbEdit': (root.userEditDlgUi.ckb_UserPermit_DefnDbEdit.isChecked()),
                                                                          'defenseAsAdmin': (root.userEditDlgUi.ckb_UserPermit_DefnAsAdmin.isChecked()),
                                                                          'plants': (root.userEditDlgUi.ckb_UserPermit_PtsScr.isChecked()),
                                                                          'plantsAsAdmin': (root.userEditDlgUi.ckb_UserPermit_PtsScr.isChecked()),
                                                                          'hardware': (root.userEditDlgUi.ckb_UserPermit_PtsAsAdmin.isChecked()),
                                                                          'hardwareAsAdmin': (root.userEditDlgUi.ckb_UserPermit_HardwareScr.isChecked()),
                                                                          'configure': (root.userEditDlgUi.ckb_UserPermit_CfgScr.isChecked()),
                                                                          'configureAsAdmin': (root.userEditDlgUi.ckb_UserPermit_CfgAsAdmin.isChecked()) } ))

                root.userEditDlg.show()
                self.userSystemLogger.debug('Диалог редактирования пользователя {0} открыт'.format(str(userToEdit.login)))

        except AttributeError:
            pass


    def callCurrentUserSetupDlg(self, root, server, usersCore, userToEdit):
        try:
            self.userSystemLogger.debug('Инициирован вызов диалога самостоятельного редактирования пользователя {0}'.format(str(userToEdit.login)))

            root.userSelfEditDlgUi.gfv_EuAvatarPrev.setPixmap(userToEdit.avatar)
            root.userSelfEditDlgUi.lbl_EuID.setText(str(userToEdit.id))
            root.userSelfEditDlgUi.lnI_EuLogin.setText(str(userToEdit.login))
            root.userSelfEditDlgUi.lnI_EuDesc.setText(str(userToEdit.description))
            root.userSelfEditDlgUi.lnI_EuAvatarAddr.setText(str(userToEdit.avatarAddress))
            
            root.userSelfEditDlgUi.filedialog = QFileDialog()
            root.userSelfEditDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
            root.userSelfEditDlgUi.filedialog.fileSelected.connect( lambda: root.userSelfEditDlgUi.lnI_EuAvatarAddr.setText(str(
                                                                    root.userSelfEditDlgUi.filedialog.selectedFiles()[0])) )

            root.userSelfEditDlgUi.tlb_Browse.clicked.connect( lambda:  root.userSelfEditDlgUi.filedialog.show() )
            root.userSelfEditDlgUi.lnI_EuAvatarAddr.textChanged.connect( lambda: root.userSelfEditDlgUi.gfv_EuAvatarPrev.setPixmap(QPixmap(QImage(str(
                                                                root.userSelfEditDlgUi.lnI_EuAvatarAddr.text())))) )
            
            root.userSelfEditDlg.accepted.connect( lambda: userToEdit.setup(usersCore, root, self.crypto.getCut(root.userSelfEditDlgUi.lnI_EuPassword.text(), bytes.fromhex(randomChoice(server.get('getUserRg', json))),
                                                                           (root.userSelfEditDlgUi.lnI_EuDesc.text()), (root.userSelfEditDlgUi.lnI_EuAvatarAddr.text()), (userToEdit.permits))))

            root.userSelfEditDlg.show()

        except AttributeError:
            pass


    def callUserDeletionDlg(self, root, userToDelete):
        try:
            self.msg = QMessageBox.question(root, 'Подтверждение действия', 'Вы действительно хотите удалить пользователя %s? Это необратимое действие!' % userToDelete.login)
            self.userSystemLogger.debug('Инициирован вызов диалога удаления пользователя {0}'.format(userToDelete.login))

            if self.msg == QMessageBox.Yes:
                if (userToDelete.type == (0 or '0') or userToDelete.description == 'Guest'):
                    self.msg = QMessageBox.critical(root, 'Действие невозможно', 'Вы не можете удалить системного пользователя!')

                else:
                    userToDelete.toDelete = True
                    self.msg = QMessageBox.information(root, 'Подтверждение операции', 'Для завершения удаления пользователя %s нажмите "Применить".' % userToDelete.login)

            elif self.msg == QMessageBox.No:
                pass

        except AttributeError:
            pass


    def generateIdForNewUser(self):
        self.aivalableUserIds = list()
        for i in range(0, 99):
            if (i >= 0) and (i < 10):
                continue
            else:
                self.aivalableUserIds.append(i)

        for User in self.users:
            try:
                self.aivalableUserIds.remove(int(User.id))
            except ValueError:
                continue

        return int(randomChoice(self.aivalableUserIds))


    def callUserCreationDlg(self, root, server, usersCore):

            self.userSystemLogger.debug('Инициирован вызов диалога создания нового пользователя')
            root.userCreationDlgUi.lbl_CnuID.setText(str(self.generateIdForNewUser()))
            root.userCreationDlgUi.lnI_CnuLogin.setText('')
            root.userCreationDlgUi.lnI_CnuPassword.setText('')
            root.userCreationDlgUi.lnI_CnuDesc.setText('')
            root.userCreationDlgUi.lnI_CnuAvatarAddr.setText('')

            root.userCreationDlgUi.filedialog = QFileDialog()
            root.userCreationDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
            root.userCreationDlgUi.filedialog.fileSelected.connect( lambda: root.userCreationDlgUi.lnI_CnuAvatarAddr.setText(str(
                                                                root.userCreationDlgUi.filedialog.selectedFiles()[0])) )

            root.userCreationDlgUi.tlb_Browse.clicked.connect( lambda:  root.userCreationDlgUi.filedialog.show() )
            root.userCreationDlgUi.lnI_CnuAvatarAddr.textChanged.connect ( lambda: root.userCreationDlgUi.gfv_CnuAvatarPrev.setPixmap(
                                                                               QPixmap(QImage(str(
                                                                               root.userCreationDlgUi.lnI_CnuAvatarAddr.text())))) )

            root.userCreationDlg.permits = dict( homeRooms = root.userCreationDlgUi.ckb_UserPermit_HomeRooms.isChecked(),
                                            homeAsAdmin = root.userCreationDlgUi.ckb_UserPermit_HomeAsAdmin.isChecked(),
                                            defenseBasic = root.userCreationDlgUi.ckb_UserPermit_DefnScr.isChecked(),
                                            defenseDbEdit = root.userCreationDlgUi.ckb_UserPermit_DefnDbEdit.isChecked(),
                                            defenseAsAdmin = root.userCreationDlgUi.ckb_UserPermit_DefnAsAdmin.isChecked(),
                                            plants = root.userCreationDlgUi.ckb_UserPermit_PtsScr.isChecked(),
                                            plantsAsAdmin = root.userCreationDlgUi.ckb_UserPermit_PtsAsAdmin.isChecked(),
                                            hardware = root.userCreationDlgUi.ckb_UserPermit_HardwareScr.isChecked(), 
                                            hardwareAsAdmin = root.userCreationDlgUi.ckb_UserPermit_HardwareAsAdmin.isChecked(),
                                            configure = root.userCreationDlgUi.ckb_UserPermit_CfgScr.isChecked(),
                                            configureAsAdmin = root.userCreationDlgUi.ckb_UserPermit_CfgAsAdmin.isChecked() )
            hmta = self.crypto.getHmta()
            server.post('updateUserRg', json, int, [0, hmta.hex()])

            root.userCreationDlg.accepted.connect ( lambda: AqUser(usersCore, root, (root.userCreationDlgUi.lbl_CnuID.text()), 
                                                                  (root.userCreationDlgUi.lnI_CnuDesc.text()), 1, (server.get('getNewUserFilename', str)), 
                                                                  (root.userCreationDlgUi.lnI_CnuAvatarAddr.text()), (root.userCreationDlgUi.lnI_CnuLogin.text()),
                                                                  (self.crypto.getCut(root.userCreationDlgUi.lnI_CnuPassword.text(), hmta)),
                                                                  (root.userCreationDlg.permits), (AqConfigSystem.loadDefaultConfigDict(AqConfigSystem))) )

            root.userCreationDlg.show()


    def getInstance(self, root, flag):

        if flag:
            self.selector = [AqUser for AqUser in self.users if (AqUser.current)]
            return self.selector[0]
        else:
            try:
                return ([AqUser for AqUser in self.users if ((root.ui.liw_UsersDbList.selectedItems()[0].text()) == AqUser.login)])[0]
            except IndexError:
                self.msg = QMessageBox.warning(root, 'Ошибка', '''Операция невозможна, так как вы не выбрали пользователя из списка.''')
    

    def updateListWidget(self, root, usersCore):
        try:
            self.selector = [AqUser for AqUser in self.users if ((root.ui.liw_UsersDbList.selectedItems()[0].text()) == AqUser.login)]
            root.ui.lbl_SelectedUserUsername.setText(self.selector[0].login)
            root.ui.lbl_SelectedUserDescription.setText(self.selector[0].description)
            root.ui.gfv_SelectedUserAvatar.setPixmap(self.selector[0].avatar)
        except IndexError:
            pass


    def logOut(self, root, server, usersCore):
        self.userSystemLogger.info('Инициирован выход из системы.')
        playsound(root.sounds['logOut'], False)

        self.loggedIn = False
        self.userSystemLogger.debug('Система пользователей перешла в состояние: (Вход в систему не произведён)')

        self.currentUser = self.getCurrentUser()
        self.currentUser.setAsCurrent(False)
        self.userSystemLogger.info('У активного пользователя ' + str(self.currentUser.login) + ' установлен параметр активности: ' + 
                                         str(self.currentUser.current))
        del self.currentUser
                
        root.ui.liw_UsersDbList.clear()
        self.userSystemLogger.info('Очистка списка пользователей')
         
        self.availableFileNames.clear()
        self.possibleFileNames.clear()
        self.cleanUserList()
        self.userSystemLogger.info('Выход из системы завершён')
        self.loadUsers(root, server, usersCore)
        self.lockApp(root, usersCore)


from _asQammDekstopLibs.config import AqConfig


class AqUser(AqUsersSystem):
    
    def __init__(self, usersCore, root, Id, Desc, Type, Filepath, AvAddr, Login, Password, Permits, ConfigDict):
       
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
           self.config = usersCore.config.loadDefaultConfig(root)
       else:
           self.config = AqConfig(ConfigDict)

       self.current = bool(False)
       self.edited = bool(True)
       self.toDelete = bool(False)

       usersCore.addToUserList(root, self, 0)


    def setup(self, usersCore, root, Password, Desc, NewAvAddr, Permits):

        self.edited = True
        self.password = Password
        self.description = Desc
        self.avatarAddress = NewAvAddr
        self.permits = Permits
        self.avatar = QPixmap((QImage(r'%s' % str(self.avatarAddress))))

        if self.current:
            root.ui.gfv_CurrentUserAvatar.setPixmap(self.avatar)
            root.ui.gfv_SelectedUserAvatar.setPixmap(self.avatar)
        else:
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


    def getDict(self):
        return {'id': self.id,
                'description': self.description,
                'type': self.type,
                'filepath': self.filepath,
                'login': self.login,
                'password': self.password,
                'avatarAddress': self.avatarAddress,
                'permits': self.permits,
                'config': self.configDict }
    