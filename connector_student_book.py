import sqlite3
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TableStudentBook(QTableView):
    def __init__(self, numer_grade_book=None):
        self.numer_grade_book = numer_grade_book
        super().__init__()
        self.create(self.numer_grade_book)

    def create(self, numer_grade_book):
        self.numer_grade_book = numer_grade_book
        model = QStandardItemModel()
        model.clear()
        model.setColumnCount(3)
        model.setHorizontalHeaderLabels(["Название", "Код книги", "Дата получения"])
        proxy = MySortFilterProxyModel()
        proxy.setSourceModel(model)
        self.setModel(proxy)
        self.setSortingEnabled(True)
        if self.numer_grade_book is not None:
            with sqlite3.connect('LIBRARY.db') as connect:
                for title, id_BOOK, date_receipt in connect.execute(f'SELECT books.title, set_books.id_BOOK, records.date_receipt '
                                                                    f'FROM books INNER JOIN set_books ON set_books.id_books = books.id_books INNER JOIN records ON records.id_book = set_books.id_BOOK '
                                                                    f'WHERE records.numer_grade_book = {self.numer_grade_book}'):
                    rows = model.rowCount()
                    model.setItem(rows, 0, QStandardItem(title))
                    model.setItem(rows, 1, QStandardItem(str(id_BOOK)))
                    model.setItem(rows, 2, QStandardItem(str(date_receipt)))
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def delete(self):
        self.model().removeRows(0, self.model().rowCount())


class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)
