from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from AsQammDekstop import AqMainWindow

from _asQammDekstopLibs.functions import AqCrypto
from _asQammDekstopLibs.config import AqConfigSystem
from _asQammDekstopLibs.logging import AqLogger

from random import choice
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

            self.userSystemLogger.Logger.info('Система пользователей успешно подготовила интерфейс приложения' + 
                                             ' для входа пользователя в систему')


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
            AqConfigSystem.applyConfig(AqConfigSystem, root, usersCore)

            root.ui.stack.setCurrentWidget(root.ui.page_1)

            self.userSystemLogger.Logger.info('Система пользователей успешно подготовила интерфейс приложения' +
                                             ' для использования пользователем {0} после успешного входа в систему'.format(str(self.currentUser.
                                                                                                                               login)))
            del self.currentUser


    def loadUsers(self, usersCore, root):

        self.userSystemLogger.Logger.info('Система пользователей начинает выполнение метода инициализации системных экземпляров' +
                                           ' класса пользователя')

        with open(r'%s' % str(self.sysFileNames[0]), 'r') as dataFile:

            fileString = dataFile.readline()
            jsonString = self.crypto.decryptContent(fileString)
            jsonString = json.loads(jsonString)
            self.userSystemLogger.Logger.debug('Прочитан ASQD-файл, получен словарь для создания экземпляра класса пользователя')

            usersCore.guest = AqUser(usersCore, root, int(jsonString['id']), (jsonString['description']), (jsonString['type']), str(self.sysFileNames[0]), 
                              (jsonString['avatarAddress']), (jsonString['login']), (jsonString['password']), str(0), (jsonString['permits']),
                              (jsonString['config']))
            usersCore.guest.edited = False


        self.userSystemLogger.Logger.info('Система пользователей начинает выполнение метода инициализации добавленных извне экземпляров' +
                                           ' класса пользователя')

        self.crypto.getFileNamesList(self.possibleFileNames)
        self.crypto.seekForFiles(root, self.possibleFileNames, self.availableFileNames, True)

        if (len(self.availableFileNames)) == 0:
                        QMessageBox.warning(root, 'Ошибка инициализации системы пользователей', 
                                            '''Не удалось найти ни одного аккаунта пользователя, за исключением аккаунта гостя. Большая часть функциональности недоступна. Проверьте, что вы создали хотя бы одного пользователя с правами админинстратора.''')

        for item in self.availableFileNames:
            with open(r'%s' % item, 'r') as dataFile:

                fileString = dataFile.readline()
                jsonString = self.crypto.decryptContent(fileString)
                jsonString = json.loads(jsonString)
                print(jsonString['password'] + ' ' + str(jsonString['hmta']))
                self.userSystemLogger.Logger.debug('Прочитан ASQD-файл, получен словарь для создания экземпляра класса пользователя')

                usersCore.instance = AqUser(usersCore, root, int(jsonString['id']), (jsonString['description']), (jsonString['type']), (str(item)),  
                              (jsonString['avatarAddress']), (jsonString['login']), (jsonString['password']), (jsonString['hmta']), (jsonString['permits']),
                              (jsonString['config']))
                usersCore.instance.edited = False
                self.userSystemLogger.Logger.info('Создан экземпляр класса пользователя: ' + str(usersCore.instance))


    def addToUserList(self, root, object, mode):
        if mode == 0:
            self.users.append(object)
            root.ui.liw_UsersDbList.addItems([object.login])
            self.userSystemLogger.Logger.debug('Экземпляр класса пользователя ({0}) был добавлен в лист экземпляров класса пользователя'.format(
                                                str(object)))
        elif mode == 1:
            for AqUser in object:
                root.ui.liw_UsersDbList.addItems([(AqUser.login)])


    def cleanUserList(self):
        self.userSystemLogger.Logger.info('Система пользователей начинает выполнение метода очистки списка экземпляров класса пользователей ' + 
                                          'после успешного входа в систему')

        self.checker = [AqUser for AqUser in self.users if (AqUser.current == False)]
        self.userSystemLogger.Logger.info('Выборка неактивных пользователей составлена')

        for AqUser in self.checker:
            self.users.remove(AqUser)

        try:
            self.userSystemLogger.Logger.info('Система пользователей успешно завершила выполнение очистки списка экземпляров класса пользователей.' + 
                                          ' В списке остаётся только активный пользователь: {0}'.format(str(self.users[0])))
        except IndexError:
            self.userSystemLogger.Logger.info('Система пользователей успешно завершила выполнение очистки списка экземпляров класса пользователей.' + 
                                          ' Список остаётся пустым, так как выполнен выход из системы')

             
    def userInit(self, root, usersCore):

        self.selector = [AqUser for AqUser in self.users if (AqUser.login == root.ui.lnI_Login.text() and
                                                             AqUser.password == self.crypto.getCut(((root.ui.lnI_Password.text()).encode('utf-8')).decode('utf-8'),
                                                             AqUser.hmta))]

        try:
            self.selector[0].setAsCurrent(True)
            self.loggedIn = True

            if self.selector[0].getPermits('pxConfigAsAdmin'):
                self.lockApp(root, usersCore)
            else:
                self.cleanUserList()
                self.lockApp(root, usersCore)
            playsound(root.sounds['login'], False)

            self.userSystemLogger.Logger.info('Вход в систему произведён')

        except IndexError:
            root.ui.box_Login.setGeometry(QtCore.QRect(360, 130, 280, 150))
            root.ui.lbl_LoginStatus.show()
            root.ui.lbl_LoginStatus.setStyleSheet('color: red;')
            root.ui.lbl_LoginStatus.setText('Неверный логин или пароль!')
            self.userSystemLogger.Logger.info('Вход в систему не произведён по причине: 0 — неверный логин или пароль')
            playsound(root.sounds['error'], False)


    def guestUserInit(self, usersCore, root):
        self.userSystemLogger.Logger.info('Система пользователей начинает выполнение метода инициализации пользователя Гость')

        usersCore.users[0].setAsCurrent(True)
        
        self.userSystemLogger.Logger.info('У активного экземпляра класса пользователя ' + str(usersCore.users[0]) + ' установлен параметр активности: ' + 
                                          str(usersCore.users[0].current) + ', экземпляр назначен активным пользователем')

        self.loggedIn = True
        self.userSystemLogger.Logger.debug('Система пользователей перешла в состояние: (Вход в систему произведён)')

        self.cleanUserList()

        self.lockApp(root, usersCore)
        self.userSystemLogger.Logger.debug('Система пользователей после входа в систему успешно завершила разблокировку интерфейса приложения')


    def callUserSetupDlg(self, root, usersCore, userToEdit):
        try:
            if (userToEdit.getPermits('pxConfigAsAdmin') and (userToEdit.current)):
                self.callCurrentUserSetupDlg(root, usersCore, userToEdit)
            else:
                self.userSystemLogger.Logger.debug('Инициирован вызов диалога редактирования пользователя {0}'.format(str(userToEdit.login)))

                root.userEditDlgUi.gfv_EuAvatarPrev.setPixmap(userToEdit.avatar)
                root.userEditDlgUi.lbl_EuID.setText(str(userToEdit.id))
                root.userEditDlgUi.lnI_EuLogin.setText(str(userToEdit.login))
                root.userEditDlgUi.lnI_EuPassword.setText(str(userToEdit.password))
                root.userEditDlgUi.lnI_EuDesc.setText(str(userToEdit.description))
                root.userEditDlgUi.lnI_EuAvatarAddr.setText(str(userToEdit.avatarAddress))

                root.userEditDlgUi.filedialog = QFileDialog()
                root.userEditDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
                root.userEditDlgUi.filedialog.fileSelected.connect( lambda: root.userEditDlgUi.lnI_EuAvatarAddr.setText(str(
                                                                        root.userEditDlgUi.filedialog.selectedFiles()[0])) )
                self.userSystemLogger.Logger.debug('Инициирован вызов QFileDialog')

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
                                       

                root.userEditDlg.accepted.connect ( lambda: userToEdit.setup(usersCore, root, (root.userEditDlgUi.lnI_EuPassword.text()), (root.userEditDlgUi.lnI_EuDesc.text()),
                                                                        (root.userEditDlgUi.lnI_EuAvatarAddr.text()),
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
                self.userSystemLogger.Logger.debug('Диалог редактирования пользователя {0} открыт'.format(str(userToEdit.login)))

        except AttributeError:
            pass


    def callCurrentUserSetupDlg(self, root, usersCore, userToEdit):
        try:
            self.userSystemLogger.Logger.debug('Инициирован вызов диалога самостоятельного редактирования пользователя {0}'.format(str(userToEdit.login)))

            root.userSelfEditDlgUi.gfv_EuAvatarPrev.setPixmap(userToEdit.avatar)
            root.userSelfEditDlgUi.lbl_EuID.setText(str(userToEdit.id))
            root.userSelfEditDlgUi.lnI_EuLogin.setText(str(userToEdit.login))
            root.userSelfEditDlgUi.lnI_EuPassword.setText(str(userToEdit.password))
            root.userSelfEditDlgUi.lnI_EuDesc.setText(str(userToEdit.description))
            root.userSelfEditDlgUi.lnI_EuAvatarAddr.setText(str(userToEdit.avatarAddress))
            
            root.userSelfEditDlgUi.filedialog = QFileDialog()
            root.userSelfEditDlgUi.filedialog.setFileMode(QFileDialog.ExistingFile)
            root.userSelfEditDlgUi.filedialog.fileSelected.connect( lambda: root.userSelfEditDlgUi.lnI_EuAvatarAddr.setText(str(
                                                                    root.userSelfEditDlgUi.filedialog.selectedFiles()[0])) )
            self.userSystemLogger.Logger.debug('Инициирован вызов QFileDialog')

            root.userSelfEditDlgUi.tlb_Browse.clicked.connect( lambda:  root.userSelfEditDlgUi.filedialog.show() )
            root.userSelfEditDlgUi.lnI_EuAvatarAddr.textChanged.connect( lambda: root.userSelfEditDlgUi.gfv_EuAvatarPrev.setPixmap(QPixmap(QImage(str(
                                                                root.userSelfEditDlgUi.lnI_EuAvatarAddr.text())))) )
            
            root.userSelfEditDlg.accepted.connect( lambda: userToEdit.setup(usersCore, root, (root.userSelfEditDlgUi.lnI_EuPassword.text()), (root.userSelfEditDlgUi.lnI_EuDesc.text()), 
                                                                       (root.userSelfEditDlgUi.lnI_EuAvatarAddr.text()), (userToEdit.permits)))

            root.userSelfEditDlg.show()
            self.userSystemLogger.Logger.debug('Диалог самостоятельного редактирования пользователя {0} открыт'.format(str(userToEdit.login)))

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


    def generateIdForNewUser(self):
        self.aivalableUserIds = list()
        for i in range(0, 99):
            if (i > 0) and (i < 10):
                continue
            else:
                self.aivalableUserIds.append(i)

        for User in self.users:
            print(User.id)
            self.aivalableUserIds.remove(int(User.id))

        return int(choice(self.aivalableUserIds))


    def callUserCreationDlg(self, root, usersCore):

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

            root.userCreationDlg.accepted.connect ( lambda: AqUser(usersCore, root, (root.userCreationDlgUi.lbl_CnuID.text()), 
                                                                  (root.userCreationDlgUi.lnI_CnuDesc.text()), 1, (self.generateFilenameForNewUser(root)), 
                                                                  (root.userCreationDlgUi.lnI_CnuAvatarAddr.text()), (root.userCreationDlgUi.lnI_CnuLogin.text()),
                                                                  (self.crypto.getCut(root.userCreationDlgUi.lnI_CnuPassword.text()), self.crypto.getHmta()),
                                                                  (self.creationDlg.permits), (AqConfigSystem.loadDefaultConfigDict(AqConfigSystem, root))) )

            root.userCreationDlg.show()


    def getInstance(self, root, flag):

        if flag:
            self.selector = [AqUser for AqUser in self.users if (AqUser.current)]
            return self.selector[0]
        else:
            try:
                self.selector = [AqUser for AqUser in self.users if ((root.ui.liw_UsersDbList.selectedItems()[0].text()) == AqUser.login)]
                print(self.selector[0])
                return self.selector[0]
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


    def logOut(self, usersCore, root):
        self.userSystemLogger.Logger.info('Инициирован выход из системы.')
        playsound(root.sounds['logOut'], False)

        self.loggedIn = False
        self.userSystemLogger.Logger.debug('Система пользователей перешла в состояние: (Вход в систему не произведён)')

        self.currentUser = self.getCurrentUser()
        self.currentUser.setAsCurrent(False)
        self.userSystemLogger.Logger.info('У активного пользователя ' + str(self.currentUser.login) + ' установлен параметр активности: ' + 
                                         str(self.currentUser.current))
        del self.currentUser
                
        root.ui.liw_UsersDbList.clear()
        self.userSystemLogger.Logger.info('Очистка списка пользователей')
         
        self.availableFileNames.clear()
        self.possibleFileNames.clear()
        self.cleanUserList()
        self.userSystemLogger.Logger.info('Система пользователей успешно завершила выход из системы')
        self.loadUsers(usersCore, root)
        self.lockApp(root, usersCore)


from _asQammDekstopLibs.config import AqConfig


class AqUser(AqUsersSystem):
    
    def __init__(self, usersCore, root, Id, Desc, Type, Filepath, AvAddr, Login, Password, Cut, Permits, ConfigDict):
       
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

       if Type == 0:
           pass
       else:
           self.hmta = (bytes.fromhex(Cut))

       if self.configPreset != None:
           self.config = usersCore.config.loadDefaultConfig(root)
       else:
           self.config = AqConfig(ConfigDict)

       self.current = bool()
       self.edited = bool(True)

       print(self.filepath)
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
    