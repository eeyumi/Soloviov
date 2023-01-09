# -*- coding: utf-8 -*-
from PyQt5 import QtSql
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QHBoxLayout, \
    QVBoxLayout, QDesktopWidget, QLabel, QTableWidget
from dialog_student import AddStudent
from dialog_book import AddBook
from connector_student import TableStudent
from connector_book import TableBook
# from connector import Connector


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Соединяем базу данных
        con_student = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con_student.setDatabaseName('LIBRARY.db')
        con_student.open()
        self.table_student = TableStudent()
        self.table_book = TableBook()
        # Задали окно
        self.setWindowTitle("Библиотека")
        self.setMinimumSize(1400, 850)
        self.center()

        """Левая сторона окна"""
        # Задаем виджеты
        search_student = QPushButton("Поиск")
        add_student = QPushButton("Добавить")
        label_student = QLabel("Студенты:")

        # Делаем горизонтальный макет
        h0_box = QHBoxLayout()
        h0_box.addStretch()
        h0_box.addWidget(add_student)
        h0_box.addWidget(search_student)
        h0_box.addStretch()

        # Делаем вертикальный макет
        v0_box = QVBoxLayout()
        v0_box.addLayout(h0_box)
        v0_box.addWidget(label_student)
        v0_box.addWidget(self.table_student)

        """Правая сторона окна"""
        # Задаем виджеты
        add_book = QPushButton("Добавить")
        search_book = QPushButton("Поиск")
        label_library = QLabel("Библиотека:")
        label_boh = QLabel(
            "Книги на руках:")  # boh - books on hand (книги на руках) P.s Да-да, с соображалкой у меня туго)))
        get_all_book = QPushButton("Забрать все")
        get_book = QPushButton("Забрать")
        give_book = QPushButton("Выдать")
        table_boh = QTableWidget()

        # Делаем горизонтальные макеты
        h1_box = QHBoxLayout()
        h1_box.addStretch()
        h1_box.addWidget(add_book)
        h1_box.addWidget(search_book)
        h1_box.addStretch()

        h2_box = QHBoxLayout()
        h2_box.addWidget(get_all_book)
        h2_box.addWidget(get_book)
        h2_box.addWidget(give_book)

        # Делаем вертикальный макет
        v1_box = QVBoxLayout()
        v1_box.addLayout(h1_box)
        v1_box.addWidget(label_library)
        v1_box.addWidget(self.table_book)
        v1_box.addWidget(label_boh)
        v1_box.addLayout(h2_box)
        v1_box.addWidget(table_boh)

        """Соединяем левую и правую часть"""
        h3_box = QHBoxLayout()
        h3_box.addLayout(v0_box)
        h3_box.addLayout(v1_box)

        # Переносим макеты в окно
        widget = QWidget()
        widget.setLayout(h3_box)
        self.setCentralWidget(widget)

        """Добавляем функционал"""
        # Кнопка добавить студента
        add_student.clicked.connect(self.update_table)

        # Кнопка добавить книгу
        add_book.clicked.connect(AddBook)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_table(self):
        AddStudent()
        self.table_student.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = Main()
    myWidget.show()
    app.exec_()
