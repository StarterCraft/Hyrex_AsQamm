from PyQt5 import QtCore, QtGui
from libs.utils import AqLogger
from libs.exceptions import ServerResponseException
import json

class AqHardwareSystem:
    def __init__(self, root, server):
        self.hardware = []

        try:
           self.hardware = server.get('getHardwareData', json)
        except ServerResponseException as exception: 
            print(exception.data[1])
            if exception.data[1] == 501: pass

        print(self.hardware)

        self.logger = AqLogger('Hardware')
        self.mainTableModel = QtGui.QStandardItemModel(0, 6)
        
        for unit in self.hardware:
            print(unit["children"])

            lu = []
            item = QtGui.QStandardItem()
            item.setText('✓' if str(unit['isEnabled']) else '❌')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item)

            item2 = QtGui.QStandardItem()
            item2.setText(unit['typeDisplayName'])
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item2)

            item3 = QtGui.QStandardItem()
            item3.setText(unit['deviceAddress'])
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item3)

            item4 = QtGui.QStandardItem()
            item4.setText('Теплица 1')
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item4)

            item5 = QtGui.QStandardItem()
            item5.setText(unit['instanceDescription'])
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item5)

            item6 = QtGui.QStandardItem()
            item6.setText(
                f'{len(unit["children"])} | {len([child for child in unit["children"].values() if child[1]["isEnabled"]])}')
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item6)

            self.mainTableModel.appendRow(lu)

        root.ui.lbl_HardwareAll.setText(str((self.getHardwareQty())[0]))
        root.ui.lbl_HardwareOnLine.setText(str((self.getHardwareQty())[1]))


    def getHardwareQty(self):
        res = [0, 0]
        for unit in self.hardware:
            res[0] += 1
            if unit['isEnabled']:
                res[1] += 1

        return res


    def setHardwareListModel(self, root):
        root.ui.tbv_HardwareList.setModel(self.mainTableModel)
        
        self.mainTableModel.setHorizontalHeaderLabels(['🔗', 'Тип', 'Порт', 'Комплекс', 'Описание', 'ПП | ПГ'])
        root.ui.tbv_HardwareList.setColumnWidth(0, 36)
        root.ui.tbv_HardwareList.setColumnWidth(1, 160)
        root.ui.tbv_HardwareList.setColumnWidth(2, 72)
        root.ui.tbv_HardwareList.setColumnWidth(3, 128)
        root.ui.tbv_HardwareList.setColumnWidth(4, 440)
        root.ui.tbv_HardwareList.setColumnWidth(5, 64)

        self.mainTableModel.itemChanged.connect( lambda: root.ui.lbl_SelectedHardwareUnit.setText(self.mainTableModel.item(self.mainTableModel.itemChanged().row(), column = 5).text()) )
