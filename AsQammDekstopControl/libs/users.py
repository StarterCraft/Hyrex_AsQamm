from libs              import AqProtectedAttribute
from PyQt5.QtWidgets   import QMessageBox, QFileDialog

from random            import choice, shuffle
from playsound         import *

import PyQt5.QtCore, PyQt5.QtGui, json, os, requests, libs.utils


class AqUsersClient:
    class PasswordChecker(libs.utils.AqThread):
        def setup(self, **kwargs):
            self.text = kwargs['passwordText']
            self.password = kwargs['userPassword']
            self.r = kwargs['bytesObjectsIter']
            self.textLabel = kwargs['loadingScreenTextLbl']
            self.exitVar = bool()


        def run(self):
            self.started.emit()

            self.textLabel.setText('Ожидание ответа сервера...')
            matches = []
            for i in self.r:
                self.textLabel.setText('Вход...')
                if self.password == libs.utils.AqCrypto.getCut(self.text, bytes.fromhex(i)):
                    matches.append(True)
                    self.exitVar = True
                    self.finished.emit()
                    self.textLabel.setText('Подготовка интерфейса...')
                    break
                else:
                    matches.append(False)
                    self.textLabel.setText('Подготовка интерфейса...')
                    continue

            if not [bool for bool in matches if (bool == True)]:
                self.exitVar = False
                self.finished.emit()
            else: pass


    class LogoutProcessor(libs.utils.AqThread):
        def setup(self, server, usersCore):
            self.server = server
            self.usersCore = usersCore


        def run(self):
            self.started.emit()

            playsound(self.root.sounds['logOut'], False)
            self.usersCore.loggedIn = False
            self.usersCore.userSystemLogger.debug('Система пользователей перешла в состояние: (Вход в систему не произведён)')

            self.usersCore.currentUser.setAsCurrent(False)
            self.usersCore.userSystemLogger.info(f'У активного пользователя {str(self.usersCore.currentUser.login)} установлен '
                                                 f'параметр активности: {str(self.usersCore.currentUser.current)}')
            self.usersCore.currentUser = None
                
            self.root.ui.liw_UsersDbList.clear()
            self.usersCore.userSystemLogger.info('Очистка списка пользователей')
         
            self.usersCore.availableFileNames.clear()
            self.usersCore.possibleFileNames.clear()
            self.usersCore.cleanUserList()
            self.usersCore.userSystemLogger.info('Выход из системы завершён')
            self.usersCore.loadUsers(self.root, self.server, self.usersCore)

            self.finished.emit()


    def __init__(self, root):
        self.crypto = libs.utils.AqCrypto()
        self.config = libs.utils.AqConfigSystem()
        self.loggedIn = bool(False)
        self.users = []
        self.sysFileNames = ["data/system/~!guest!~.asqd"]
        self.userSystemLogger = libs.utils.AqLogger('UserSystem')
        self.possibleFileNames = []
        self.availableFileNames = []


    def getCurrentUser(self):
        if self.currentUser != None:
            return self.currentUser


    def setCurrentUser(self, root, user):
        self.currentUser = user
        root.ui.lbl_CurrentUserUsername.setText(user.login.value)
        root.ui.lbl_CurrentUserDescription.setText(user.description)
        root.ui.gfv_CurrentUserAvatar.setPixmap(user.avatar)
        

    def lockApp(self, root, server, usersCore):
        if not self.loggedIn:
            root.ui.frame_top.hide()
            root.ui.frame_left_menu.hide()
            root.ui.box_Login.setGeometry(PyQt5.QtCore.QRect(500, 120, 280, 130))
            root.ui.lbl_LoginStatus.hide()

            root.ui.btn_Toggle.setEnabled(False)
            root.ui.btn_HomePage.setEnabled(False)
            root.ui.btn_DefensePage.setEnabled(False)
            root.ui.btn_PlantsPage.setEnabled(False)
            root.ui.btn_HardwarePage.setEnabled(False)
            root.ui.btn_SettingsPage.setEnabled(False)

            root.ui.btn_Apply.setEnabled(False)
            root.ui.btn_Save.setEnabled(False)
            root.ui.btn_Load.setEnabled(False)

            root.ui.lnI_Login.setText('')
            root.ui.lnI_Password.setText('')

            root.ui.stack.setCurrentWidget(root.ui.page_Login)

            self.userSystemLogger.info('Интерфейс приложения подготовлен для входа пользователя в систему')


        elif self.loggedIn:
            currentUser = self.getCurrentUser()

            root.ui.lbl_PageName.setText('Наш дом')
            root.ui.lbl_CurrentUserUsername.setText(currentUser.login.value)
            root.ui.lbl_CurrentUserDescription.setText(currentUser.description)
            root.ui.gfv_CurrentUserAvatar.setPixmap(currentUser.avatar)

            root.ui.frame_top.show()
            root.ui.frame_left_menu.show()
            root.ui.box_Login.setGeometry(PyQt5.QtCore.QRect(450, 110, 280, 130))

            root.ui.btn_Toggle.setEnabled(True)
            root.ui.btn_HomePage.setEnabled(True)

            if currentUser.getPermits('pxDefnBasic'): root.ui.btn_DefensePage.setEnabled(True)
            else: root.ui.btn_DefensePage.setEnabled(False)

            if currentUser.getPermits('pxPlants'): root.ui.btn_PlantsPage.setEnabled(True)
            else: root.ui.btn_PlantsPage.setEnabled(False)

            if currentUser.getPermits('pxHardware'): root.ui.btn_HardwarePage.setEnabled(True)
            else: root.ui.btn_HardwarePage.setEnabled(False)

            if currentUser.getPermits('pxConfig'): root.ui.btn_SettingsPage.setEnabled(True)
            else: root.ui.btn_SettingsPage.setEnabled(False)

            if currentUser.getPermits('pxConfigAsAdmin'):
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
            libs.utils.AqConfigSystem.applyConfig(root, server, usersCore)

            if currentUser.configPreset != 'default':
                libs.utils.AqUIFunctions.loadSpecifiedTheme(root, currentUser.config.theme)
            else: pass

            root.ui.stack.setCurrentWidget(root.ui.page_Home)

            del currentUser


    def loadUsers(self, root, server, usersCore):
        with open(rf'{str(self.sysFileNames[0])}', 'r') as dataFile:
            fileString = dataFile.readline()
            jsonString = self.crypto.decryptContent(fileString)
            jsonString = json.loads(jsonString)

            usersCore.guest = AqUser(usersCore, root, int(jsonString['id']), (jsonString['description']), (jsonString['type']), str(self.sysFileNames[0]), 
                              (jsonString['avatarAddress']), (jsonString['login']), (jsonString['password']), (jsonString['permits']),
                              (jsonString['config']))
            usersCore.guest.edited = False

        self.userSystemLogger.info('Начата загрузка аккаунтов пользователей...')
        
        r = server.get('getUserdata', json)
        server.commutatorLogger.debug('Данные с сервера загружены')

        if not len(list(r)):
            libs.utils.AqUIFunctions.showMessageBox(libs.utils.AqUIFunctions, root, libs.utils.AqUIFunctions.CriticalMessageboxLevel,
                'Ошибка инициализации системы пользователей', 
                'Не удалось найти ни одного аккаунта пользователя, за исключением аккаунта гостя. '
                'Большая часть функциональности недоступна. Проверьте, что вы создали хотя бы одного '
                'пользователя с правами админинстратора.')

        for item in r:
            try:
                if self.currentUser.login == (item['login']): #Если логин текущего пользователя совпадает с загруженным
                    usersCore.instance = AqUser(usersCore, root, int(item['id']), (item['description']), (item['type']), (item['filepath']),  
                                      (item['avatarAddress']), (item['login']), (item['password']), (item['permits']), (item['config']))
                    usersCore.setCurrentUser(root, usersCore.instance)
                    usersCore.instance.edited = False
                    self.userSystemLogger.debug('Загружен пользователь ' + str(usersCore.instance.login))

                else: #Если логин текущего пользователя НЕ совпадает с загруженным
                    usersCore.instance = AqUser(usersCore, root, int(item['id']), (item['description']), (item['type']), (item['filepath']),  
                                      (item['avatarAddress']), (item['login']), (item['password']), (item['permits']), (item['config']))
                    usersCore.instance.edited = False
                    self.userSystemLogger.debug('Загружен пользователь ' + str(usersCore.instance.login))

            except (AttributeError, RuntimeError): #Сюда попадём, если вход ещё не выполнялся
                usersCore.instance = AqUser(usersCore, root, int(item['id']), (item['description']), (item['type']), (item['filepath']),  
                                  (item['avatarAddress']), (item['login']), (item['password']), (item['permits']), (item['config']))
                usersCore.instance.edited = False
                self.userSystemLogger.debug('Загружен пользователь ' + str(usersCore.instance.login))

        del r


    def addToUserList(self, root, object, mode):
        if mode == 0:
            self.users.append(object)
            root.ui.liw_UsersDbList.addItems([object.login.value])
            
        elif mode == 1:
            for AqUser in object: root.ui.liw_UsersDbList.addItems([AqUser.login.value])


    def cleanUserList(self):
        self.checker = [AqUser for AqUser in self.users if (AqUser.current == False)]
        for AqUser in self.checker: self.users.remove(AqUser)
           
             
    def userInit(self, root, server, usersCore):
        self.selector = [AqUser for AqUser in self.users if (AqUser.login == root.ui.lnI_Login.text())]
        self.matches = []
        exiter = bool()
        self.userSystemLogger.debug(f'Инициирован вход в систему как {root.ui.lnI_Login.text()}')

        r = server.get('getUserRg', json)
        try:
            paThread =    self.PasswordChecker(root, passwordText         = root.ui.lnI_Password.text(),
                                                     userPassword         = self.selector[0].password,
                                                     bytesObjectsIter     = r,
                                                     loadingScreenTextLbl = root.ui.lbl_LoadingText)
            paThread.started.connect( lambda: libs.utils.AqUIFunctions.showLoadingAnimation(root) )
            paThread.finished.connect( lambda: self.userCheck(root, server, usersCore, paThread.exitVar) )
            paThread.start()

        except IndexError:
            libs.utils.AqUIFunctions.hideLoadingAnimation(root, root.ui.page_Login)
            root.ui.box_Login.setGeometry(PyQt5.QtCore.QRect(500, 120, 280, 150))
            root.ui.lbl_LoginStatus.show()
            root.ui.lbl_LoginStatus.setStyleSheet('color: red;')
            root.ui.lbl_LoginStatus.setText('Неверный логин или пароль!')
            self.userSystemLogger.info('Вход в систему не произведён по причине: 0 — неверный логин или пароль')
            playsound(root.sounds['error'], False)
            
        shuffle(r)
        server.post('updateUserRg', json, int, [1, r])
        del r


    def userCheck(self, root, server, usersCore, boolean):
        if boolean:
            libs.utils.AqUIFunctions.hideLoadingAnimation(root, root.ui.page_Home)
            self.selector[0].setAsCurrent(True)
            self.setCurrentUser(root, self.selector[0])
            self.selector[0].edited = False
            self.loggedIn = True

            if self.selector[0].getPermits('pxConfigAsAdmin'): self.lockApp(root, server, usersCore)
            else:
                self.cleanUserList()
                self.lockApp(root, server, usersCore)
                    
            playsound(root.sounds['login'], False)
            self.userSystemLogger.info(f'Вход в систему произведён пользователем {self.selector[0].login}')

        else:
            libs.utils.AqUIFunctions.hideLoadingAnimation(root, root.ui.page_Login)
            root.ui.box_Login.setGeometry(PyQt5.QtCore.QRect(500, 120, 280, 150))
            root.ui.lbl_LoginStatus.show()
            root.ui.lbl_LoginStatus.setStyleSheet('color: red;')
            root.ui.lbl_LoginStatus.setText('Неверный логин или пароль!')
            self.userSystemLogger.info('Вход в систему не произведён по причине: 0 — неверный логин или пароль')
            playsound(root.sounds['error'], False)
                

    def guestUserInit(self, usersCore, server, root):
        usersCore.users[0].setAsCurrent(True)
        self.userSystemLogger.info(f'У активного пользователя (Гость) установлен параметр активности: {usersCore.users[0].current}, экземпляр назначен активным пользователем')

        self.loggedIn = True
        self.cleanUserList()
        self.currentUser = self.users[0]
        playsound(root.sounds['login'], False)
        self.lockApp(root, server, usersCore)

        self.userSystemLogger.info('Вход в систему произведён в режиме гостя')


    def callUserSetupDlg(self, root, server, usersCore, userToEdit):
        try:
            if (userToEdit.getPermits('pxConfigAsAdmin') and (userToEdit.current)):
                self.callCurrentUserSetupDlg(root, usersCore, userToEdit)
            else:
                self.userSystemLogger.debug(f'Инициирован вызов диалога редактирования пользователя {userToEdit.login}')

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
                root.userEditDlgUi.lnI_EuAvatarAddr.textChanged.connect( lambda: root.userEditDlgUi.gfv_EuAvatarPrev.setPixmap(
                    PyQt5.QtGui.QPixmap(PyQt5.QtGui.QImage(root.userEditDlgUi.lnI_EuAvatarAddr.text()))) )

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
                                       
                hmta = self.crypto.getHmta()
                server.post('updateUserRg', json, int, [0, hmta.hex()])
                root.userEditDlg.accepted.connect(
                    lambda: userToEdit.setup(usersCore, root, self.crypto.getCut(root.userSelfEditDlgUi.lnI_EuPassword.text(), hmta),
                            root.userEditDlgUi.lnI_EuDesc.text(), root.userEditDlgUi.lnI_EuAvatarAddr.text(),
                            { 'homeRooms': root.userEditDlgUi.ckb_UserPermit_HomeRooms.isChecked(),
                              'homeAsAdmin': root.userEditDlgUi.ckb_UserPermit_HomeAsAdmin.isChecked(),
                              'defenseBasic': root.userEditDlgUi.ckb_UserPermit_DefnScr.isChecked(),
                              'defenseDbEdit': root.userEditDlgUi.ckb_UserPermit_DefnDbEdit.isChecked(),
                              'defenseAsAdmin': root.userEditDlgUi.ckb_UserPermit_DefnAsAdmin.isChecked(),
                              'plants': root.userEditDlgUi.ckb_UserPermit_PtsScr.isChecked(),
                              'plantsAsAdmin': root.userEditDlgUi.ckb_UserPermit_PtsScr.isChecked(),
                              'hardware': root.userEditDlgUi.ckb_UserPermit_PtsAsAdmin.isChecked(),
                              'hardwareAsAdmin': root.userEditDlgUi.ckb_UserPermit_HardwareScr.isChecked(),
                              'configure': root.userEditDlgUi.ckb_UserPermit_CfgScr.isChecked(),
                              'configureAsAdmin': root.userEditDlgUi.ckb_UserPermit_CfgAsAdmin.isChecked()}))

                root.userEditDlg.show()
                self.userSystemLogger.debug(f'Диалог редактирования пользователя {userToEdit.login} открыт')

        except AttributeError:
            pass


    def callCurrentUserSetupDlg(self, root, server, usersCore, userToEdit):
        try:
            self.userSystemLogger.debug(f'Инициирован вызов диалога самостоятельного редактирования пользователя {userToEdit.login}')

            root.userSelfEditDlgUi.gfv_EuAvatarPrev.setPixmap(userToEdit.avatar)
            root.userSelfEditDlgUi.lbl_EuID.setText(str(userToEdit.id))
            root.userSelfEditDlgUi.lnI_EuLogin.setText(userToEdit.login.value)
            root.userSelfEditDlgUi.lnI_EuDesc.setText(userToEdit.description)
            root.userSelfEditDlgUi.lnI_EuAvatarAddr.setText(userToEdit.avatarAddress)
            
            root.userSelfEditDlgUi.filedialog = QFileDialog()
            root.userSelfEditDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
            root.userSelfEditDlgUi.filedialog.fileSelected.connect( lambda: root.userSelfEditDlgUi.lnI_EuAvatarAddr.setText(str(
                                                                    root.userSelfEditDlgUi.filedialog.selectedFiles()[0])) )

            root.userSelfEditDlgUi.tlb_Browse.clicked.connect( lambda:  root.userSelfEditDlgUi.filedialog.show() )
            root.userSelfEditDlgUi.lnI_EuAvatarAddr.textChanged.connect(
                lambda: root.userSelfEditDlgUi.gfv_EuAvatarPrev.setPixmap(
                    PyQt5.QtGui.QPixmap(PyQt5.QtGui.QImage(root.userSelfEditDlgUi.lnI_EuAvatarAddr.text()))) )
            
            root.userSelfEditDlg.accepted.connect(
                lambda: userToEdit.setup(
                    usersCore, root, self.crypto.getCut(root.userSelfEditDlgUi.lnI_EuPassword.text(),
                    bytes.fromhex(choice(server.get('getUserRg', json)))), root.userSelfEditDlgUi.lnI_EuDesc.text(), 
                    root.userSelfEditDlgUi.lnI_EuAvatarAddr.text(), userToEdit.permits))

            root.userSelfEditDlg.show()

        except AttributeError: pass


    def callUserDeletionDlg(self, root, userToDelete):
        try:
            self.msg = QMessageBox.question(root, 'Подтверждение действия', rf'Вы действительно хотите удалить пользователя {userToDelete.login}? Это необратимое действие!')
            self.userSystemLogger.debug(f'Инициирован вызов диалога удаления пользователя {userToDelete.login}')

            if self.msg == QMessageBox.Yes:
                if (userToDelete.type == (0 or '0') or userToDelete.description == 'Guest'):
                    self.msg = QMessageBox.critical(root, 'Действие невозможно', 'Вы не можете удалить системного пользователя!')
                elif (userToDelete.current):
                    self.msg = QMessageBox.critical(root, 'Действие невозможно', 'Вы не можете удалить аккаунт пользователя, '
                        'через который выполнен вход!')
                else:
                    userToDelete.toDelete = True
                    self.msg = QMessageBox.information(root, 'Подтверждение операции', 
                        f'Для завершения удаления пользователя {userToDelete.login} нажмите "Применить".')

            elif self.msg == QMessageBox.No: return

        except AttributeError: return


    def generateIdForNewUser(self):
        self.aivalableUserIds = list()
        for i in range(0, 99):
            if (i >= 0) and (i < 10): continue
            else: self.aivalableUserIds.append(i)

        for User in self.users:
            try: self.aivalableUserIds.remove(int(User.id))
            except ValueError: continue

        return int(choice(self.aivalableUserIds))


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
            root.userCreationDlgUi.lnI_CnuAvatarAddr.textChanged.connect(
                lambda: root.userCreationDlgUi.gfv_CnuAvatarPrev.setPixmap(
                    PyQt5.QtGui.QPixmap(PyQt5.QtGui.QImage(root.userCreationDlgUi.lnI_CnuAvatarAddr.text()))) )

            hmta = self.crypto.getHmta()
            print(hmta.hex())
            server.post('updateUserRg', json, int, [0, hmta.hex()])

            root.userCreationDlg.accepted.connect(
                lambda:  AqUser(usersCore, root, (root.userCreationDlgUi.lbl_CnuID.text()), 
                               (root.userCreationDlgUi.lnI_CnuDesc.text()), 1, (server.get('getNewUserFilename', str)), 
                               (root.userCreationDlgUi.lnI_CnuAvatarAddr.text()), (root.userCreationDlgUi.lnI_CnuLogin.text()),
                               (self.crypto.getCut(root.userCreationDlgUi.lnI_CnuPassword.text(), hmta)),
                               {'homeRooms' : root.userCreationDlgUi.ckb_UserPermit_HomeRooms.isChecked(),
                                'homeAsAdmin' : root.userCreationDlgUi.ckb_UserPermit_HomeAsAdmin.isChecked(),
                                'defenseBasic' : root.userCreationDlgUi.ckb_UserPermit_DefnScr.isChecked(),
                                'defenseDbEdit' : root.userCreationDlgUi.ckb_UserPermit_DefnDbEdit.isChecked(),
                                'defenseAsAdmin' : root.userCreationDlgUi.ckb_UserPermit_DefnAsAdmin.isChecked(),
                                'plants' : root.userCreationDlgUi.ckb_UserPermit_PtsScr.isChecked(),
                                'plantsAsAdmin' : root.userCreationDlgUi.ckb_UserPermit_PtsAsAdmin.isChecked(),
                                'hardware' : root.userCreationDlgUi.ckb_UserPermit_HardwareScr.isChecked(), 
                                'hardwareAsAdmin' : root.userCreationDlgUi.ckb_UserPermit_HardwareAsAdmin.isChecked(),
                                'configure' : root.userCreationDlgUi.ckb_UserPermit_CfgScr.isChecked(),
                                'configureAsAdmin' : root.userCreationDlgUi.ckb_UserPermit_CfgAsAdmin.isChecked()},
                                {'preset': 'default'}) )

            root.userCreationDlg.show()


    def getInstance(self, root, flag):
        if flag:
            self.selector = [AqUser for AqUser in self.users if AqUser.current]
            return self.selector[0]
        else:
            try:
                return [AqUser for AqUser in self.users if (root.ui.liw_UsersDbList.selectedItems()[0].text()) == AqUser.login][0]
            except IndexError:
                self.msg = QMessageBox.warning(root, 'Ошибка', '''Операция невозможна, так как вы не выбрали пользователя из списка.''')
    

    def updateListWidget(self, root, usersCore):
        try:
            self.selector = [AqUser for AqUser in self.users if root.ui.liw_UsersDbList.selectedItems()[0].text() == AqUser.login]
            root.ui.lbl_SelectedUserUsername.setText(self.selector[0].login.value)
            root.ui.lbl_SelectedUserDescription.setText(self.selector[0].description)
            root.ui.gfv_SelectedUserAvatar.setPixmap(self.selector[0].avatar)
        except IndexError: pass


    def logOutBegin(self, root, server, usersCore):
        self.userSystemLogger.info('Инициирован выход из системы.')
        libs.utils.AqUIFunctions.showLoadingAnimation(root)
        myThread = self.LogoutProcessor(root, server, usersCore)
        myThread.finished.connect( lambda: self.logOutLock(root, server, usersCore) )
        myThread.start()


    def logOutLock(self, root, server, usersCore):
        self.lockApp(root, server, usersCore)
        libs.utils.AqUIFunctions.hideLoadingAnimation(root, root.ui.page_Login)


class AqUser:    
    def __init__(self, usersCore, root, Id, Desc, Type, Filepath, AvAddr, Login, Password, Permits, ConfigDict):       
        self.id = Id
        self.type = Type
        self.filepath = Filepath
        self.description = Desc
        self.avatarAddress = AvAddr
        self.avatar = PyQt5.QtGui.QPixmap(PyQt5.QtGui.QImage(fr'{self.avatarAddress}'))
        self.login = AqProtectedAttribute(Login)
        self.password = AqProtectedAttribute(Password)
        self.permits = AqProtectedAttribute(Permits)
        self.configDict = ConfigDict
        self.configPreset = ConfigDict['preset']
       
        if self.configPreset != None:
            self.config = usersCore.config.loadDefaultConfig(root)
        else:
            self.config = libs.utils.AqConfig(ConfigDict)

        self.current = bool(False)
        self.edited = bool(True)
        self.toDelete = bool(False)

        usersCore.addToUserList(root, self, 0)


    def setup(self, usersCore, root, Password, Desc, NewAvAddr, Permits):
        self.edited = True
        self.description = Desc
        self.avatarAddress = NewAvAddr
        self.avatar = PyQt5.QtGui.QPixmap(PyQt5.QtGui.QImage(fr'{self.avatarAddress}'))
        self.password = AqProtectedAttribute(Password)
        self.permits = AqProtectedAttribute(Permits)

        if self.current:
            root.ui.gfv_CurrentUserAvatar.setPixmap(self.avatar)
            root.ui.gfv_SelectedUserAvatar.setPixmap(self.avatar)
            root.ui.lbl_SelectedUserDescription.setText(self.description)
        else:
            root.ui.gfv_SelectedUserAvatar.setPixmap(self.avatar)
            root.ui.lbl_SelectedUserDescription.setText(self.description)


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
    