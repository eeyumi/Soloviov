from PyQt5 import QtSql
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TableStudent(QTableView):
    def __init__(self, squad=None, course=None):
        super().__init__()
        self.squad = squad
        self.course = course
        self.create(self.squad, self.course)
    def create(self, squad, course):
        self.squad = squad
        self.course = course
        model = QStandardItemModel()
        model.clear()
        print(self.squad, self.course)
        if self.squad is not None and self.course is not None:
            query = QtSql.QSqlQuery(f"""SELECT fullname, squad, course FROM students WHERE squad='{squad}' AND course='{course}'""")
        elif self.squad is not None:
            query = QtSql.QSqlQuery(f"""SELECT fullname, squad, course FROM students WHERE squad='{squad}'""")
        elif self.course is not None:
            query = QtSql.QSqlQuery(f"""SELECT fullname, squad, course FROM students WHERE course='{course}'""")

        if self.squad is None and self.course is None:
            query = QtSql.QSqlQuery("""SELECT fullname, squad, course FROM students""")
        model.setColumnCount(3)
        model.setHorizontalHeaderLabels(["ФИО", "Группа", "Курс"])
        proxy = MySortFilterProxyModel()
        proxy.setSourceModel(model)
        self.setModel(proxy)
        self.setSortingEnabled(True)
        while query.next():
            rows = model.rowCount()
            # model.setRowCount(rows + 1)
            model.setItem(rows, 0, QStandardItem(query.value(0)))
            model.setItem(rows, 1, QStandardItem(query.value(1)))
            model.setItem(rows, 2, QStandardItem(str(query.value(2))))
        self.setFixedWidth(670)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def delete(self):
        self.model().removeRows(0, self.model().rowCount())
class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)
