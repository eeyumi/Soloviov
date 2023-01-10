
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class SearchBook(QTableView):
    def __init__(self, title):
        super().__init__()
        model = QStandardItemModel()
        query = QSqlQuery()
        query.exec(f""" SELECT title, release, type_book FROM books
             WHERE (title) LIKE ('%{title}%') COLLATE NOCASE""")

        model.setColumnCount(3)
        model.setHorizontalHeaderLabels(["Название книги", "Дата выпуска", "Тип книги"])
        proxy = MySortFilterProxyModel()
        proxy.setSourceModel(model)
        self.setModel(proxy)
        self.setSortingEnabled(True)
        while query.next():
            rows = model.rowCount()
            model.setRowCount(rows + 1)
            model.setItem(rows, 0, QStandardItem(query.value(0)))
            model.setItem(rows, 1, QStandardItem(str(query.value(1))))
            model.setItem(rows, 2, QStandardItem(query.value(2)))
        self.setFixedWidth(1200)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        if (source_left.isValid() and source_right.isValid()):
            if (source_left.column() == 1):  # <== номер колонки с числами
                return int(source_left.data()) < int(source_right.data())
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)
