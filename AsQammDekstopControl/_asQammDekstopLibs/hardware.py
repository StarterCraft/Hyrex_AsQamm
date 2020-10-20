from PyQt5 import QtCore, QtGui
from _asQammDekstopLibs.functions import AqLogger
import json

class AqHardwareSystem:
    def __init__(self, root, server):
        self.hardware = server.get('getHardwareData', json)
        print(self.hardware)
        self.logger = AqLogger('Hardware')
        self.mainTableModel = QtGui.QStandardItemModel(0, 4)
        self.mainTableModel.setHorizontalHeaderLabels(['Тип', 'Порт', 'Комплекс', 'Описание', 'МП | МГ'])
        
        root.ui.tbv_HardwareList.setColumnWidth(0, 30)
        root.ui.tbv_HardwareList.setColumnWidth(1, 20)
        root.ui.tbv_HardwareList.setColumnWidth(2, 35)
        root.ui.tbv_HardwareList.setColumnWidth(3, 300)
        root.ui.tbv_HardwareList.setColumnWidth(4, 30)
        root.ui.tbv_HardwareList.horizontalHeader().resizeSections()
        
        for unit in self.hardware:
            lu = []
            item = QtGui.QStandardItem()
            item.setText(unit['unitType'])
            lu.append(item)

            item2 = QtGui.QStandardItem()
            item2.setText(unit['comPort'])
            item2.setTextAlignment(QtCore.Qt.AlignHCenter)
            lu.append(item2)

            item3 = QtGui.QStandardItem()
            item3.setText('')
            item3.setTextAlignment(QtCore.Qt.AlignHCenter)

            item4 = QtGui.QStandardItem()
            item4.setText(unit['description'])
            lu.append(item4)

            item5 = QtGui.QStandardItem()
            item5.setText(f'{unit["modulesQty"]} | {unit["enabledQty"]}')
            item5.setTextAlignment(QtCore.Qt.AlignHCenter)
            lu.append(item5)

            self.mainTableModel.appendRow(lu)
            