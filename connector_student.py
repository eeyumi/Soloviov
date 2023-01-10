from PyQt5 import QtSql
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TableStudent(QTableView):
    def __init__(self, squad=None, course=None):
        super().__init__()
        model = QStandardItemModel()
        model.clear()
        print(squad, course)
        if squad is not None and course is not None:
            query = QtSql.QSqlQuery(f"""SELECT fullname, squad, course FROM students WHERE squad='{squad}' AND course='{course}'""")
        elif squad is not None:
            query = QtSql.QSqlQuery(f"""SELECT fullname, squad, course FROM students WHERE squad='{squad}'""")
        elif course is not None:
            query = QtSql.QSqlQuery(f"""SELECT fullname, squad, course FROM students WHERE course='{course}'""")

        if squad is None and course is None:
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
        self.setFixedWidth(800)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)


class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        if (source_left.isValid() and source_right.isValid()):
            if (source_left.column() == 2):  # <== номер колонки с числами
                return int(source_left.data()) < int(source_right.data())
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)
