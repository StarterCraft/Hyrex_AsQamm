# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data\err.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 230)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data\\error.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet("QDialog { background-color: rgb(45, 45, 45); color: white; }\n"
"\n"
"QGroupBox { font: 10pt \"Segoe UI Semibold\"; color: white; }\n"
"\n"
"QCheckBox, QLabel { font: 9pt \"Segoe UI Semilight\"; color: white; }\n"
"QCheckBox:disabled { color: gray; }\n"
"\n"
"/*  QScrollBar::vertical */\n"
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
"/*  QScrollBar::horizontal */\n"
"QScrollBar:horizontal\n"
" {\n"
"     height: 15px;\n"
"     margin: 3px 15px 3px 15px;\n"
"     border: 1px transparent #2A2929;\n"
"     background-color: #2A2929;    \n"
" }\n"
"\n"
" QScrollBar::handle:horizontal\n"
" {\n"
"     background-color: rgb(45, 45, 45);      \n"
"     min-width: 5px;\n"
"     border: 2px solid white;\n"
"     border-radius: 4px;\n"
" }\n"
"\n"
" QScrollBar::add-line:horizontal\n"
" {\n"
"     margin: 0px 3px 0px 3px;\n"
"     border-image: url(./images/right_arrow_disabled.png);       \n"
"     width: 10px;\n"
"     height: 10px;\n"
"     subcontrol-position: right;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::sub-line:horizontal\n"
" {\n"
"     margin: 0px 3px 0px 3px;\n"
"     border-image: url(./images/left_arrow_disabled.png);        \n"
"     height: 10px;\n"
"     width: 10px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on\n"
" {\n"
"     border-image: url(./images/right_arrow.png);               \n"
"     height: 10px;\n"
"     width: 10px;\n"
"     subcontrol-position: right;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on\n"
" {\n"
"     border-image: url(./images/left_arrow.png);               \n"
"     height: 10px;\n"
"     width: 10px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
" {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
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
"    font: 8pt \"Segoe UI Semilight\";\n"
" }\n"
"\n"
"QLineEdit:hover { \n"
"    border-color: rgb(42, 105, 23);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lbl_ErrorSign = QtWidgets.QLabel(self.frame)
        self.lbl_ErrorSign.setGeometry(QtCore.QRect(6, 18, 80, 80))
        self.lbl_ErrorSign.setText("")
        self.lbl_ErrorSign.setPixmap(QtGui.QPixmap(":/error.ico"))
        self.lbl_ErrorSign.setScaledContents(True)
        self.lbl_ErrorSign.setObjectName("lbl_ErrorSign")
        self.lbl_ErrorTitle = QtWidgets.QLabel(self.frame)
        self.lbl_ErrorTitle.setGeometry(QtCore.QRect(100, 12, 281, 18))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_ErrorTitle.setFont(font)
        self.lbl_ErrorTitle.setStyleSheet("font:  11pt \"Segoe UI Semibold\"")
        self.lbl_ErrorTitle.setText("")
        self.lbl_ErrorTitle.setScaledContents(False)
        self.lbl_ErrorTitle.setObjectName("lbl_ErrorTitle")
        self.lbl_ErrorDesc = QtWidgets.QLabel(self.frame)
        self.lbl_ErrorDesc.setGeometry(QtCore.QRect(100, 40, 281, 111))
        self.lbl_ErrorDesc.setText("")
        self.lbl_ErrorDesc.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_ErrorDesc.setWordWrap(True)
        self.lbl_ErrorDesc.setObjectName("lbl_ErrorDesc")
        self.lnI_lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lnI_lineEdit.setGeometry(QtCore.QRect(100, 150, 281, 20))
        self.lnI_lineEdit.setObjectName("lnI_lineEdit")
        self.lbl_lineEditTitle = QtWidgets.QLabel(self.frame)
        self.lbl_lineEditTitle.setGeometry(QtCore.QRect(0, 150, 91, 16))
        self.lbl_lineEditTitle.setText("")
        self.lbl_lineEditTitle.setObjectName("lbl_lineEditTitle")
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_OpenCrashReport = QtWidgets.QPushButton(Dialog)
        self.btn_OpenCrashReport.setMinimumSize(QtCore.QSize(80, 24))
        self.btn_OpenCrashReport.setObjectName("btn_OpenCrashReport")
        self.horizontalLayout.addWidget(self.btn_OpenCrashReport)
        self.btn_Accept = QtWidgets.QPushButton(Dialog)
        self.btn_Accept.setMinimumSize(QtCore.QSize(80, 24))
        self.btn_Accept.setObjectName("btn_Accept")
        self.horizontalLayout.addWidget(self.btn_Accept)
        self.btn_Close = QtWidgets.QPushButton(Dialog)
        self.btn_Close.setMinimumSize(QtCore.QSize(80, 24))
        self.btn_Close.setObjectName("btn_Close")
        self.horizontalLayout.addWidget(self.btn_Close)
        self.btn_OpenSessionLog = QtWidgets.QPushButton(Dialog)
        self.btn_OpenSessionLog.setMinimumSize(QtCore.QSize(80, 24))
        self.btn_OpenSessionLog.setObjectName("btn_OpenSessionLog")
        self.horizontalLayout.addWidget(self.btn_OpenSessionLog)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.btn_Close.clicked.connect(Dialog.reject)
        self.btn_Accept.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Обработчик ошибок AsQamm"))
        self.lnI_lineEdit.setPlaceholderText(_translate("Dialog", "{адрес} или {адрес}:{порт}"))
        self.btn_OpenCrashReport.setToolTip(_translate("Dialog", "Просмотреть очёт об ошибке"))
        self.btn_OpenCrashReport.setText(_translate("Dialog", "Просмотр"))
        self.btn_Accept.setToolTip(_translate("Dialog", "Отправить отчёт об ошибке в Hyrex и закрыть"))
        self.btn_Accept.setText(_translate("Dialog", "Отправить"))
        self.btn_Close.setToolTip(_translate("Dialog", "Не отправлять отчёт об ошибке в Hyrex и закрыть"))
        self.btn_Close.setText(_translate("Dialog", "Закрыть"))
        self.btn_OpenSessionLog.setToolTip(_translate("Dialog", "Просмотреть журнал сессии"))
        self.btn_OpenSessionLog.setText(_translate("Dialog", "Журнал"))
import req_rc
