# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userCreation.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dlg_CreateNewUserInUserDb(object):
    def setupUi(self, Dlg_CreateNewUserInUserDb):
        Dlg_CreateNewUserInUserDb.setObjectName("Dlg_CreateNewUserInUserDb")
        Dlg_CreateNewUserInUserDb.resize(401, 477)
        Dlg_CreateNewUserInUserDb.setWindowOpacity(0.9595)
        Dlg_CreateNewUserInUserDb.setStyleSheet("QDialog { background-color: rgb(45, 45, 45); color: white; }\n"
"\n"
"QGroupBox { font: 10pt \"Segoe UI Semibold\"; color: white; }\n"
"\n"
"QCheckBox, QLabel { font: 9pt \"Segoe UI Semilight\"; color: white; }\n"
"QCheckBox:disabled { color: gray; }\n"
"\n"
"\n"
" QScrollBar:vertical\n"
" {\n"
"     background-color: #2A2929;\n"
"     width: 15px;\n"
"     margin: 15px 3px 15px 3px;\n"
"     border: 1px transparent #2A2929;\n"
" }\n"
"\n"
"\n"
" QScrollBar::handle:vertical\n"
" {\n"
"     background-color: rgb(45, 45, 45);         /* #605F5F; */\n"
"     min-height: 5px;\n"
"     border: 2px solid white;\n"
"     border-radius: 4px;\n"
" }\n"
"\n"
"\n"
" QScrollBar::sub-line:vertical\n"
" {\n"
"     margin: 3px 0px 3px 0px;\n"
"     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
"     height: 10px;\n"
"     width: 10px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
"\n"
" QScrollBar::add-line:vertical\n"
" {\n"
"     margin: 3px 0px 3px 0px;\n"
"     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
"     height: 10px;\n"
"     width: 10px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
"\n"
" QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on\n"
" {\n"
"\n"
"     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
"     height: 10px;\n"
"     width: 10px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
"\n"
" QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on\n"
" {\n"
"     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
"     height: 10px;\n"
"     width: 10px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
"\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
" {\n"
"     background: none;\n"
" }\n"
"\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
" {\n"
"     background: none;\n"
" }\n"
"\n"
"\n"
"QComboBox {\n"
"    color: black;\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 3px;\n"
"    min-width: 6em;\n"
"    font: 8pt \"Segoe UI Semilight\";\n"
"}\n"
"\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid rgb(254, 254, 254);\n"
"    background-color: rgb(236, 236, 236);\n"
"}\n"
"\n"
"\n"
"QPushButton { \n"
"    color: black;\n"
"    background-color: rgb(215, 215, 215);\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;  \n"
"    min-width: 6em;\n"
"    font: 8pt \"Segoe UI Semibold\";\n"
"}\n"
"\n"
"\n"
"QPushButton:hover { \n"
"    background-color: rgb(235, 235, 235);\n"
"}\n"
"\n"
"\n"
"QPushButton:pressed { \n"
"    background-color: rgb(221, 221, 221);\n"
"}\n"
"\n"
"QComboBox:disabled { color: gray; background-color: rgb(35, 35, 35); }\n"
"\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/images/arrowDown_ico.png);\n"
"}\n"
"\n"
"\n"
"QComboBox::up-arrow { image: url(:/images/arrowUp_ico.png); }\n"
"\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"\n"
"QComboBox:!editable, QComboBox::drop-down:editable {\n"
"     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"}\n"
"\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
"                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
"}\n"
"\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"\n"
"QLineEdit { \n"
"    border-radius: 3px;\n"
"    border: 1px solid white;\n"
" }\n"
"\n"
"QLineEdit:hover { \n"
"    border-color: rgb(42, 105, 23);\n"
"}")
        Dlg_CreateNewUserInUserDb.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dlg_CreateNewUserInUserDb)
        self.verticalLayout.setObjectName("verticalLayout")
        self.box_MainUserProps = QtWidgets.QGroupBox(Dlg_CreateNewUserInUserDb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_MainUserProps.sizePolicy().hasHeightForWidth())
        self.box_MainUserProps.setSizePolicy(sizePolicy)
        self.box_MainUserProps.setObjectName("box_MainUserProps")
        self.gridLayout = QtWidgets.QGridLayout(self.box_MainUserProps)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_CnuAvatarPrevHint = QtWidgets.QLabel(self.box_MainUserProps)
        self.lbl_CnuAvatarPrevHint.setObjectName("lbl_CnuAvatarPrevHint")
        self.gridLayout.addWidget(self.lbl_CnuAvatarPrevHint, 1, 0, 1, 1)
        self.lbl_CnuPassword = QtWidgets.QLabel(self.box_MainUserProps)
        self.lbl_CnuPassword.setObjectName("lbl_CnuPassword")
        self.gridLayout.addWidget(self.lbl_CnuPassword, 5, 0, 1, 1)
        self.lbl_CnuLogin = QtWidgets.QLabel(self.box_MainUserProps)
        self.lbl_CnuLogin.setObjectName("lbl_CnuLogin")
        self.gridLayout.addWidget(self.lbl_CnuLogin, 4, 0, 1, 1)
        self.lbl_CnuAvatarHint = QtWidgets.QLabel(self.box_MainUserProps)
        self.lbl_CnuAvatarHint.setObjectName("lbl_CnuAvatarHint")
        self.gridLayout.addWidget(self.lbl_CnuAvatarHint, 6, 0, 1, 1)
        self.lbl_CnuID = QtWidgets.QLabel(self.box_MainUserProps)
        self.lbl_CnuID.setObjectName("lbl_CnuID")
        self.gridLayout.addWidget(self.lbl_CnuID, 3, 1, 1, 1)
        self.lbl_CnuIDHint = QtWidgets.QLabel(self.box_MainUserProps)
        self.lbl_CnuIDHint.setObjectName("lbl_CnuIDHint")
        self.gridLayout.addWidget(self.lbl_CnuIDHint, 3, 0, 1, 1)
        self.tlb_Browse = QtWidgets.QToolButton(self.box_MainUserProps)
        self.tlb_Browse.setObjectName("tlb_Browse")
        self.gridLayout.addWidget(self.tlb_Browse, 6, 3, 1, 1)
        self.gfv_CnuAvatarPrev = QtWidgets.QLabel(self.box_MainUserProps)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gfv_CnuAvatarPrev.sizePolicy().hasHeightForWidth())
        self.gfv_CnuAvatarPrev.setSizePolicy(sizePolicy)
        self.gfv_CnuAvatarPrev.setMinimumSize(QtCore.QSize(64, 64))
        self.gfv_CnuAvatarPrev.setMaximumSize(QtCore.QSize(64, 64))
        self.gfv_CnuAvatarPrev.setStyleSheet("border: 1px solid grey;")
        self.gfv_CnuAvatarPrev.setText("")
        self.gfv_CnuAvatarPrev.setScaledContents(True)
        self.gfv_CnuAvatarPrev.setWordWrap(False)
        self.gfv_CnuAvatarPrev.setObjectName("gfv_CnuAvatarPrev")
        self.gridLayout.addWidget(self.gfv_CnuAvatarPrev, 1, 1, 1, 1)
        self.lnI_CnuAvatarAddr = QtWidgets.QLineEdit(self.box_MainUserProps)
        self.lnI_CnuAvatarAddr.setObjectName("lnI_CnuAvatarAddr")
        self.gridLayout.addWidget(self.lnI_CnuAvatarAddr, 6, 1, 1, 2)
        self.lbl_CnuDesc = QtWidgets.QLabel(self.box_MainUserProps)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_CnuDesc.sizePolicy().hasHeightForWidth())
        self.lbl_CnuDesc.setSizePolicy(sizePolicy)
        self.lbl_CnuDesc.setObjectName("lbl_CnuDesc")
        self.gridLayout.addWidget(self.lbl_CnuDesc, 7, 0, 1, 1)
        self.btn_CnuAvatarPrevRef = QtWidgets.QPushButton(self.box_MainUserProps)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_CnuAvatarPrevRef.sizePolicy().hasHeightForWidth())
        self.btn_CnuAvatarPrevRef.setSizePolicy(sizePolicy)
        self.btn_CnuAvatarPrevRef.setMinimumSize(QtCore.QSize(64, 18))
        self.btn_CnuAvatarPrevRef.setMaximumSize(QtCore.QSize(64, 18))
        self.btn_CnuAvatarPrevRef.setObjectName("btn_CnuAvatarPrevRef")
        self.gridLayout.addWidget(self.btn_CnuAvatarPrevRef, 2, 1, 1, 1)
        self.lnI_CnuLogin = QtWidgets.QLineEdit(self.box_MainUserProps)
        self.lnI_CnuLogin.setObjectName("lnI_CnuLogin")
        self.gridLayout.addWidget(self.lnI_CnuLogin, 4, 1, 1, 3)
        self.lnI_CnuPassword = QtWidgets.QLineEdit(self.box_MainUserProps)
        self.lnI_CnuPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lnI_CnuPassword.setObjectName("lnI_CnuPassword")
        self.gridLayout.addWidget(self.lnI_CnuPassword, 5, 1, 1, 3)
        self.lnI_CnuDesc = QtWidgets.QLineEdit(self.box_MainUserProps)
        self.lnI_CnuDesc.setObjectName("lnI_CnuDesc")
        self.gridLayout.addWidget(self.lnI_CnuDesc, 7, 1, 1, 3)
        self.verticalLayout.addWidget(self.box_MainUserProps)
        self.box_UserPermits = QtWidgets.QGroupBox(Dlg_CreateNewUserInUserDb)
        self.box_UserPermits.setObjectName("box_UserPermits")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.box_UserPermits)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cbb_UserPermit_4 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_4.setChecked(True)
        self.cbb_UserPermit_4.setObjectName("cbb_UserPermit_4")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_4, 7, 0, 1, 1)
        self.cbb_UserPermit_7 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_7.setEnabled(False)
        self.cbb_UserPermit_7.setObjectName("cbb_UserPermit_7")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_7, 4, 1, 1, 1)
        self.cbb_UserPermit_2 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_2.setObjectName("cbb_UserPermit_2")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_2, 1, 0, 1, 1)
        self.cbb_UserPermit_8 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_8.setChecked(True)
        self.cbb_UserPermit_8.setObjectName("cbb_UserPermit_8")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_8, 7, 1, 1, 1)
        self.cbb_UserPermit_9 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_9.setObjectName("cbb_UserPermit_9")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_9, 8, 0, 1, 1)
        self.cbb_UserPermit_6 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_6.setEnabled(False)
        self.cbb_UserPermit_6.setObjectName("cbb_UserPermit_6")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_6, 1, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.box_UserPermits)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 5, 0, 1, 2)
        self.cbb_UserPermit_1 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_1.setEnabled(False)
        self.cbb_UserPermit_1.setCheckable(True)
        self.cbb_UserPermit_1.setChecked(True)
        self.cbb_UserPermit_1.setObjectName("cbb_UserPermit_1")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_1, 0, 0, 1, 1)
        self.cbb_UserPermit_3 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_3.setObjectName("cbb_UserPermit_3")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_3, 4, 0, 1, 1)
        self.cbb_UserPermit_5 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_5.setObjectName("cbb_UserPermit_5")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_5, 0, 1, 1, 1)
        self.cbb_UserPermit_10 = QtWidgets.QCheckBox(self.box_UserPermits)
        self.cbb_UserPermit_10.setObjectName("cbb_UserPermit_10")
        self.gridLayout_2.addWidget(self.cbb_UserPermit_10, 8, 1, 1, 1)
        self.verticalLayout.addWidget(self.box_UserPermits)
        self.btb_Buttons = QtWidgets.QDialogButtonBox(Dlg_CreateNewUserInUserDb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btb_Buttons.sizePolicy().hasHeightForWidth())
        self.btb_Buttons.setSizePolicy(sizePolicy)
        self.btb_Buttons.setMaximumSize(QtCore.QSize(16777215, 32))
        self.btb_Buttons.setStyleSheet("min-height: 24px;")
        self.btb_Buttons.setLocale(QtCore.QLocale(QtCore.QLocale.Russian, QtCore.QLocale.Russia))
        self.btb_Buttons.setOrientation(QtCore.Qt.Horizontal)
        self.btb_Buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.btb_Buttons.setCenterButtons(True)
        self.btb_Buttons.setObjectName("btb_Buttons")
        self.verticalLayout.addWidget(self.btb_Buttons)

        self.retranslateUi(Dlg_CreateNewUserInUserDb)
        self.btb_Buttons.accepted.connect(Dlg_CreateNewUserInUserDb.accept)
        self.btb_Buttons.rejected.connect(Dlg_CreateNewUserInUserDb.reject)
        self.cbb_UserPermit_1.toggled['bool'].connect(self.cbb_UserPermit_2.setEnabled)
        self.cbb_UserPermit_5.toggled['bool'].connect(self.cbb_UserPermit_6.setEnabled)
        self.cbb_UserPermit_5.toggled['bool'].connect(self.cbb_UserPermit_7.setEnabled)
        self.cbb_UserPermit_4.toggled['bool'].connect(self.cbb_UserPermit_9.setEnabled)
        self.cbb_UserPermit_8.toggled['bool'].connect(self.cbb_UserPermit_10.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dlg_CreateNewUserInUserDb)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.btn_CnuAvatarPrevRef, self.lnI_CnuLogin)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.lnI_CnuLogin, self.lnI_CnuPassword)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.lnI_CnuPassword, self.lnI_CnuAvatarAddr)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.lnI_CnuAvatarAddr, self.tlb_Browse)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.tlb_Browse, self.lnI_CnuDesc)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.lnI_CnuDesc, self.cbb_UserPermit_1)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_1, self.cbb_UserPermit_2)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_2, self.cbb_UserPermit_3)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_3, self.cbb_UserPermit_4)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_4, self.cbb_UserPermit_9)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_9, self.cbb_UserPermit_5)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_5, self.cbb_UserPermit_6)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_6, self.cbb_UserPermit_7)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_7, self.cbb_UserPermit_8)
        Dlg_CreateNewUserInUserDb.setTabOrder(self.cbb_UserPermit_8, self.cbb_UserPermit_10)

    def retranslateUi(self, Dlg_CreateNewUserInUserDb):
        _translate = QtCore.QCoreApplication.translate
        Dlg_CreateNewUserInUserDb.setWindowTitle(_translate("Dlg_CreateNewUserInUserDb", "Создать нового пользователя AsQamm"))
        self.box_MainUserProps.setTitle(_translate("Dlg_CreateNewUserInUserDb", "Основные настройки"))
        self.lbl_CnuAvatarPrevHint.setText(_translate("Dlg_CreateNewUserInUserDb", "Просмотр:"))
        self.lbl_CnuPassword.setText(_translate("Dlg_CreateNewUserInUserDb", "Пароль:"))
        self.lbl_CnuLogin.setText(_translate("Dlg_CreateNewUserInUserDb", "Логин:"))
        self.lbl_CnuAvatarHint.setText(_translate("Dlg_CreateNewUserInUserDb", "Аватарка:"))
        self.lbl_CnuID.setText(_translate("Dlg_CreateNewUserInUserDb", "(id)"))
        self.lbl_CnuIDHint.setText(_translate("Dlg_CreateNewUserInUserDb", "ID:"))
        self.tlb_Browse.setText(_translate("Dlg_CreateNewUserInUserDb", "..."))
        self.lbl_CnuDesc.setText(_translate("Dlg_CreateNewUserInUserDb", "Описание:"))
        self.btn_CnuAvatarPrevRef.setText(_translate("Dlg_CreateNewUserInUserDb", "Обновить"))
        self.box_UserPermits.setTitle(_translate("Dlg_CreateNewUserInUserDb", "Настройки разрешений"))
        self.cbb_UserPermit_4.setText(_translate("Dlg_CreateNewUserInUserDb", "Экран \"Оборудование\""))
        self.cbb_UserPermit_7.setText(_translate("Dlg_CreateNewUserInUserDb", "Управление системой защиты"))
        self.cbb_UserPermit_2.setText(_translate("Dlg_CreateNewUserInUserDb", "Управление комнатами"))
        self.cbb_UserPermit_8.setText(_translate("Dlg_CreateNewUserInUserDb", "Экран \"Конфигурация\""))
        self.cbb_UserPermit_9.setText(_translate("Dlg_CreateNewUserInUserDb", "Доб/удл. оборудование"))
        self.cbb_UserPermit_6.setText(_translate("Dlg_CreateNewUserInUserDb", "Изменение БД защиты"))
        self.cbb_UserPermit_1.setToolTip(_translate("Dlg_CreateNewUserInUserDb", "Отключить возможность открытия экрана статистики дома нельзя, так как это - базовая функциональность"))
        self.cbb_UserPermit_1.setText(_translate("Dlg_CreateNewUserInUserDb", "Экран \"Статистика дома\""))
        self.cbb_UserPermit_3.setText(_translate("Dlg_CreateNewUserInUserDb", "Экран \"Растения\""))
        self.cbb_UserPermit_5.setText(_translate("Dlg_CreateNewUserInUserDb", "Защита"))
        self.cbb_UserPermit_10.setText(_translate("Dlg_CreateNewUserInUserDb", "Настройки суперадмина"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dlg_CreateNewUserInUserDb = QtWidgets.QDialog()
    ui = Ui_Dlg_CreateNewUserInUserDb()
    ui.setupUi(Dlg_CreateNewUserInUserDb)
    Dlg_CreateNewUserInUserDb.show()
    sys.exit(app.exec_())