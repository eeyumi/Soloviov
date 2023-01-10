import sqlite3
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class TableBook(QTableView):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        model = QStandardItemModel()
        model.setColumnCount(4)
        model.setHorizontalHeaderLabels(["Название книги", "Автор", "Дата выпуска", "Тип книги"])
        proxy = MySortFilterProxyModel()
        proxy.setSourceModel(model)
        self.setModel(proxy)
        self.setSortingEnabled(True)
        with sqlite3.connect('LIBRARY.db') as connect:
            for title, name, release, type_book in connect.execute(
                    'SELECT books.title, authors.name, books.release, books.type_book FROM books JOIN books_authors ON books_authors.id_books = books.id_books JOIN authors ON authors.id_author = books_authors.id_author'):
                rows = model.rowCount()
                model.setRowCount(rows + 1)
                model.setItem(rows, 0, QStandardItem(title))
                model.setItem(rows, 1, QStandardItem(name))
                model.setItem(rows, 2, QStandardItem(str(release)))
                model.setItem(rows, 3, QStandardItem(type_book))
        self.setFixedWidth(1200)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def delete(self):
        self.model().removeRows(0, self.model().rowCount())

    def search_book(self, title):
        self.title = title
        model = QStandardItemModel()
        model.setColumnCount(4)
        model.setHorizontalHeaderLabels(["Название книги", "Автор", "Дата выпуска", "Тип книги"])
        proxy = MySortFilterProxyModel()
        proxy.setSourceModel(model)
        self.setModel(proxy)
        self.setSortingEnabled(True)
        with sqlite3.connect('LIBRARY.db') as connect:
            for titles, name, release, type_book in connect.execute(f"SELECT books.title, authors.name, books.release, books.type_book FROM books JOIN books_authors ON books_authors.id_books = books.id_books JOIN authors ON authors.id_author = books_authors.id_author WHERE title like '%{self.title}%'"):
                rows = model.rowCount()
                # model.setRowCount(rows + 1)
                model.setItem(rows, 0, QStandardItem(titles))
                model.setItem(rows, 1, QStandardItem(name))
                model.setItem(rows, 2, QStandardItem(str(release)))
                model.setItem(rows, 3, QStandardItem(type_book))
        self.setFixedWidth(1200)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)


class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)
