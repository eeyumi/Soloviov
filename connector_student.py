from PyQt5 import QtSql
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TableStudent(QTableView):
    def __init__(self):
        super().__init__()
        model = QStandardItemModel()
        query = QtSql.QSqlQuery("""SELECT fullname, squad, course FROM students""")
        model.setColumnCount(3)
        model.setHorizontalHeaderLabels(["ФИО", "Группа", "Курс"])
        proxy = MySortFilterProxyModel()
        proxy.setSourceModel(model)
        self.setModel(proxy)
        self.setSortingEnabled(True)
        while query.next():
            rows = model.rowCount()
            model.setRowCount(rows + 1)
            model.setItem(rows, 0, QStandardItem(query.value(0)))
            model.setItem(rows, 1, QStandardItem(query.value(1)))
            model.setItem(rows, 2, QStandardItem(str(query.value(2))))
        self.resizeColumnsToContents()


class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        if (source_left.isValid() and source_right.isValid()):
            if (source_left.column() == 2):  # <== номер колонки с числами
                return int(source_left.data()) < int(source_right.data())
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)
