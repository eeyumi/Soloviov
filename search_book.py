import sqlite3
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class SearchBook(QTableView):
    def __init__(self, title):
        super().__init__()
        model = QStandardItemModel()
        model.setColumnCount(4)
        model.setHorizontalHeaderLabels(["Название книги", "Автор", "Дата выпуска", "Тип книги"])
        proxy = MySortFilterProxyModel()
        proxy.setSourceModel(model)
        self.setModel(proxy)
        self.setSortingEnabled(True)
        with sqlite3.connect('LIBRARY.db') as connect:
            for titles, name, release, type_book in connect.execute(f"SELECT books.title, authors.name, books.release, books.type_book FROM books JOIN books_authors ON books_authors.id_books = books.id_books JOIN authors ON authors.id_author = books_authors.id_author WHERE title like '%{title}%'"):
                rows = model.rowCount()
                model.setRowCount(rows + 1)
                model.setItem(rows, 0, QStandardItem(titles))
                model.setItem(rows, 1, QStandardItem(name))
                model.setItem(rows, 2, QStandardItem(str(release)))
                model.setItem(rows, 3, QStandardItem(type_book))
        self.setFixedWidth(1200)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        if (source_left.isValid() and source_right.isValid()):
            if (source_left.column() == 2):  # <== номер колонки с числами
                return int(source_left.data()) < int(source_right.data())
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)
