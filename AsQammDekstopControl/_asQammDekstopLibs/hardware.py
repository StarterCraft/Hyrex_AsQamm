from PyQt5 import QtCore, QtGui
from _asQammDekstopLibs.functions import AqLogger
import json

class AqHardwareSystem:
    def __init__(self, root, server):
        self.hardware = server.get('getHardwareData', json)
        self.logger = AqLogger('Hardware')
        self.mainTableModel = QtGui.QStandardItemModel(0, 6)
        
        for unit in self.hardware:
            lu = []
            item = QtGui.QStandardItem()
            item.setText(str(unit['isEnabled']))
            lu.append(item)

            item2 = QtGui.QStandardItem()
            item2.setText(unit['unitType'])
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item2)

            item3 = QtGui.QStandardItem()
            item3.setText(unit['comPort'])
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item3)

            item4 = QtGui.QStandardItem()
            item4.setText('Теплица 1')
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item4)

            item5 = QtGui.QStandardItem()
            item5.setText(unit['description'])
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            lu.append(item5)

            item6 = QtGui.QStandardItem()
            item6.setText(f'{unit["modulesQty"]} | {unit["enabledQty"]}')
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
        
        self.mainTableModel.setHorizontalHeaderLabels(['ВКЛ', 'Тип', 'Порт', 'Комплекс', 'Описание', 'МП | МГ'])
        root.ui.tbv_HardwareList.setColumnWidth(0, 36)
        root.ui.tbv_HardwareList.setColumnWidth(1, 96)
        root.ui.tbv_HardwareList.setColumnWidth(2, 72)
        root.ui.tbv_HardwareList.setColumnWidth(3, 128)
        root.ui.tbv_HardwareList.setColumnWidth(4, 480)
        root.ui.tbv_HardwareList.setColumnWidth(5, 64)

        self.mainTableModel.itemChanged.connect( lambda: root.ui.lbl_SelectedHardwareUnit.setText(self.mainTableModel.item(self.mainTableModel.itemChanged().row(), column = 5).text()) )
