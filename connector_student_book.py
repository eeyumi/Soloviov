import sqlite3
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TableStudentBook(QTableView):
    def __init__(self, numer_grade_book=None):
        super().__init__()
        model = QStandardItemModel()
        model.clear()
        model.setColumnCount(3)
        model.setHorizontalHeaderLabels(["Название", "Код книги", "Дата получения"])
        proxy = MySortFilterProxyModel()
        proxy.setSourceModel(model)
        self.setModel(proxy)
        self.setSortingEnabled(True)
        if numer_grade_book is not None:
            with sqlite3.connect('LIBRARY.db') as connect:
                for title, id_BOOK, date_receipt in connect.execute(f"""SELECT books.title, set_books.id_BOOK, records.date_receipt FROM books INNER JOIN set_books ON set_books.id_books = books.id_books INNER JOIN records ON records.id_book = set_books.id_BOOK WHERE records.numer_grade_book = {numer_grade_book} AND records.return_date IS NULL"""):
                    rows = model.rowCount()
                    model.setRowCount(rows + 1)
                    model.setItem(rows, 0, QStandardItem(title))
                    model.setItem(rows, 1, QStandardItem(str(id_BOOK)))
                    model.setItem(rows, 2, QStandardItem(str(date_receipt[:10])))
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
