#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import QSortFilterProxyModel

class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        if (source_left.isValid() and source_right.isValid()):
            if (source_left.column() == 1):    # <== номер колонки с числами
                return int(source_left.data()) < int(source_right.data())
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setGeometry(300, 200, 500, 400)

        w_view = QTableView(self)
        w_model = QStandardItemModel(self)
        w_model.setHorizontalHeaderLabels(['Деталь', 'Длина', 'Поставщик'])
        w_proxy = MySortFilterProxyModel(self)
        w_proxy.setSourceModel(w_model)
        w_view.setModel(w_proxy)
        w_view.setSortingEnabled(True)

        rows = [['Стойка', 200, 'Фабрика'],
                ['Штанга', 10, 'Завод'],
                ['Перекладина', 5, 'Мастерская']
               ]

        for row in rows:
            w_model.appendRow([QStandardItem(row[0]),
                               QStandardItem(str(row[1])),
                               QStandardItem(row[2])])
        self.setCentralWidget(w_view)

myapp = QApplication(sys.argv)
window = Window()
window.show()

myapp.exec_()
sys.exit()