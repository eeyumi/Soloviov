# -*- coding: utf-8 -*-
from PyQt5 import QtSql
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, QLineEdit, QComboBox, qApp, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from dialog_student import AddStudent
from dialog_book import AddBook
from connector_student import TableStudent
from connector_book import TableBook
from connector_student_book import TableStudentBook
from search_book import SearchBook
from interface import Connect


# from connector import Connector


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Соединяем базу данных
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('LIBRARY.db')
        db.open()
        self.table_student = TableStudent()
        self.table_book = TableBook()
        self.table_boh = TableStudentBook()
        # Задали окно
        self.setWindowTitle("Библиотека")
        # self.showFullScreen()

        """Левая сторона окна"""
        # Задаем виджеты
        # search_student = QPushButton("Поиск")
        add_student = QPushButton("Добавить студента")
        self.del_student = QPushButton("Удалить студента")
        label_student = QLabel("Студенты:")
        self.combo_squad = QComboBox()
        self.combo_course = QComboBox()
        self.combo_squad.addItems(["Группа", "ПМФ", "БЭК", "ПМ", "АВТ", "ЦТ", "ИТ", "ВТ", "ТМ", "ДП", "ЭП"])
        self.combo_course.addItems(["Курс", "1", "2", "3", "4"])

        # Делаем горизонтальный макет
        h0_box = QHBoxLayout()
        h0_box.addStretch()
        h0_box.addWidget(add_student)
        h0_box.addWidget(self.del_student)
        h0_box.addWidget(self.combo_squad)
        h0_box.addWidget(self.combo_course)
        h0_box.addStretch()

        # Делаем вертикальный макет
        self.v0_box = QVBoxLayout()
        self.v0_box.addLayout(h0_box)
        self.v0_box.addWidget(label_student)
        self.v0_box.addWidget(self.table_student)

        """Правая сторона окна"""
        # Задаем виджеты
        add_book = QPushButton("Добавить книгу")
        self.del_book = QPushButton("Удалить книгу")
        lable_book = QLabel("Найти по названию книги: ")
        self.line_search_book = QLineEdit()
        label_library = QLabel("Библиотека:")
        self.label_books_hand = QLabel("Книги на руках:")  # boh - books on hand (книги на руках) P.s Да-да, с соображалкой у меня туго)))
        get_all_book = QPushButton("Забрать все")
        get_book = QPushButton("Забрать")
        give_book = QPushButton("Выдать")
        exit = QPushButton("Выход")
        self.line_id_book = QLineEdit()
        label_id_book = QLabel("Укажите код книги: ")

        # Задаем ввод для зачетки
        reg_number = QRegExp("[0-9]{6,6}")
        validator_number = QRegExpValidator(reg_number)
        self.line_id_book.setValidator(validator_number)

        # Делаем горизонтальные макеты
        h1_box = QHBoxLayout()
        h1_box.addStretch()
        h1_box.addWidget(add_book)
        h1_box.addWidget(self.del_book)
        h1_box.addWidget(lable_book)
        h1_box.addWidget(self.line_search_book)
        h1_box.addStretch()
        h1_box.addWidget(exit)

        h2_box = QHBoxLayout()
        h2_box.addWidget(get_all_book)
        h2_box.addWidget(get_book)
        h2_box.addWidget(give_book)

        h4_box = QHBoxLayout()
        h4_box.addWidget(self.label_books_hand, 2)
        # h4_box.addStretch()
        h4_box.addWidget(label_id_book)
        h4_box.addWidget(self.line_id_book)

        # Делаем вертикальный макет
        self.v1_box = QVBoxLayout()
        self.v1_box.addLayout(h1_box)
        self.v1_box.addWidget(label_library)
        self.v1_box.addWidget(self.table_book)
        self.v1_box.addLayout(h4_box)
        self.v1_box.addLayout(h2_box)
        self.v1_box.addWidget(self.table_boh)

        """Соединяем левую и правую часть"""
        h3_box = QHBoxLayout()
        h3_box.addLayout(self.v0_box)
        h3_box.addLayout(self.v1_box)

        # Переносим макеты в окно
        widget = QWidget()
        widget.setLayout(h3_box)
        self.setCentralWidget(widget)

        """Добавляем функционал"""
        add_student.clicked.connect(self.update_add_table_student)
        # self.del_book.clicked.connect(self.update_del_table_book)
        add_book.clicked.connect(self.update_add_table_book)
        # add_book.clicked.connect(self.update_add_table_book)
        exit.clicked.connect(qApp.quit)
        self.combo_squad.currentTextChanged.connect(self.update_table)
        self.combo_course.currentTextChanged.connect(self.update_table)
        self.table_student.clicked.connect(self.clicked_row_student)
        self.table_book.clicked.connect(self.clicked_row_book)
        self.table_book.doubleClicked.connect(self.clicked_row_book)

        self.line_search_book.textEdited.connect(self.search_book)
        self.del_student.clicked.connect(lambda: self.update_del_table_student(self.numer_grade_book))
        self.del_book.clicked.connect(self.update_del_table_book)

    def search_book(self):
        self.v1_box.removeWidget(self.table_book)
        self.table_book = SearchBook(self.line_search_book.text())
        self.v1_box.insertWidget(2, self.table_book)
        self.table_book.clicked.connect(self.clicked_row_book)

    def clicked_row_book(self, r):
        column = r.column()
        if column != 0:
            column = 0
        a = Connect()
        self.id_books = a.set_book_student(self.table_book.model().index(r.row(), column).data(),
                                            self.table_book.model().index(r.row(), column + 1).data(),
                                            self.table_book.model().index(r.row(), column + 2).data())[0]


    def clicked_row_student(self, r):
        column = r.column()
        if column != 0:
            column = 0
        a = Connect()
        self.numer_grade_book = (a.get_student(self.table_student.model().index(r.row(), column).data(),
                                               self.table_student.model().index(r.row(), column + 1).data(),
                                               self.table_student.model().index(r.row(), column + 2).data())[0])
        print(self.numer_grade_book)
        self.label_books_hand.setText("Книги на руках: " + self.table_student.model().index(r.row(), column).data())
        self.v1_box.removeWidget(self.table_boh)
        self.table_boh = TableStudentBook(self.numer_grade_book)
        self.v1_box.insertWidget(5, self.table_boh)

    def update_add_table_student(self):
        AddStudent()
        self.update_table()

    def update_del_table_student(self, numer_grade_book):
        student = Connect()
        result_del = student.delete_student(numer_grade_book)
        print(result_del)
        if result_del:
            self.update_table()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            msg.setText("У студента на руках есть книги!\nДля удаления студента этих книг быть не должно!!!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def update_table(self):
        self.v0_box.removeWidget(self.table_student)
        self.table_student = TableStudent(
            None if self.combo_squad.currentText() == "Группа" else self.combo_squad.currentText(),
            None if self.combo_course.currentText() == "Курс" else self.combo_course.currentText())
        self.v0_box.insertWidget(2, self.table_student)
        self.table_student.clicked.connect(self.clicked_row_student)

    def update_table_book_student(self):
        self.v1_box.removeWidget(self.table_boh)
        self.table_boh = TableStudentBook()
        self.v1_box.insertWidget(2, self.table_boh)
        self.table_boh.clicked.connect(self.clicked_row_student)

    def update_add_table_book(self):
        AddBook()
        self.v1_box.removeWidget(self.table_book)
        self.table_book = TableBook()
        self.v1_box.insertWidget(2, self.table_book)
        self.table_book.clicked.connect(self.clicked_row_book)

    def update_del_table_book(self):
        student = Connect()
        result_del = student.delete_book(self.id_books)
        print(result_del)
        self.v1_box.removeWidget(self.table_book)
        self.table_book = TableBook()
        self.v1_box.insertWidget(2, self.table_book)
        self.table_book.clicked.connect(self.clicked_row_book)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = Main()
    myWidget.show()
    app.exec_()
