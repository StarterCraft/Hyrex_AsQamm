# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uisrc\applyChanges.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dlg_ApplyChanges(object):
    def setupUi(self, Dlg_ApplyChanges):
        Dlg_ApplyChanges.setObjectName("Dlg_ApplyChanges")
        Dlg_ApplyChanges.resize(400, 200)
        Dlg_ApplyChanges.setWindowOpacity(0.9595)
        Dlg_ApplyChanges.setStyleSheet("QDialog { background-color: rgb(45, 45, 45); color: white; }\n"
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
" }\n"
"\n"
"QLineEdit:hover { \n"
"    border-color: rgb(42, 105, 23);\n"
"}")
        Dlg_ApplyChanges.setSizeGripEnabled(False)
        Dlg_ApplyChanges.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dlg_ApplyChanges)
        self.verticalLayout.setObjectName("verticalLayout")
        self.box_MainUserProps = QtWidgets.QGroupBox(Dlg_ApplyChanges)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_MainUserProps.sizePolicy().hasHeightForWidth())
        self.box_MainUserProps.setSizePolicy(sizePolicy)
        self.box_MainUserProps.setObjectName("box_MainUserProps")
        self.gridLayout = QtWidgets.QGridLayout(self.box_MainUserProps)
        self.gridLayout.setContentsMargins(-1, 3, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.box_MainUserProps)
        self.treeWidget.setStyleSheet("QTreeView, QHeaderView::section { background-color: rgb(45, 45, 45); color: white; border: none; }")
        self.treeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.treeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.treeWidget.setAutoExpandDelay(-1)
        self.treeWidget.setIndentation(20)
        self.treeWidget.setItemsExpandable(False)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setDefaultSectionSize(39)
        self.treeWidget.header().setHighlightSections(True)
        self.treeWidget.header().setStretchLastSection(True)
        self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.box_MainUserProps)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_Accept = QtWidgets.QPushButton(Dlg_ApplyChanges)
        self.btn_Accept.setMinimumSize(QtCore.QSize(80, 24))
        self.btn_Accept.setObjectName("btn_Accept")
        self.horizontalLayout_3.addWidget(self.btn_Accept)
        self.btn_Decline = QtWidgets.QPushButton(Dlg_ApplyChanges)
        self.btn_Decline.setMinimumSize(QtCore.QSize(80, 24))
        self.btn_Decline.setObjectName("btn_Decline")
        self.horizontalLayout_3.addWidget(self.btn_Decline)
        spacerItem1 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dlg_ApplyChanges)
        self.btn_Accept.clicked.connect(Dlg_ApplyChanges.accept)
        self.btn_Decline.clicked.connect(Dlg_ApplyChanges.reject)
        QtCore.QMetaObject.connectSlotsByName(Dlg_ApplyChanges)

    def retranslateUi(self, Dlg_ApplyChanges):
        _translate = QtCore.QCoreApplication.translate
        Dlg_ApplyChanges.setWindowTitle(_translate("Dlg_ApplyChanges", "Сохранение изменений"))
        self.box_MainUserProps.setTitle(_translate("Dlg_ApplyChanges", "Выберите изменения, которые хотите сохранить:"))
        self.treeWidget.headerItem().setText(0, _translate("Dlg_ApplyChanges", "сохр."))
        self.treeWidget.headerItem().setText(1, _translate("Dlg_ApplyChanges", "Объект"))
        self.btn_Accept.setText(_translate("Dlg_ApplyChanges", "Сохранить"))
        self.btn_Decline.setText(_translate("Dlg_ApplyChanges", "Отменить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dlg_ApplyChanges = QtWidgets.QDialog()
    ui = Ui_Dlg_ApplyChanges()
    ui.setupUi(Dlg_ApplyChanges)
    Dlg_ApplyChanges.show()
    sys.exit(app.exec_())