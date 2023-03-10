# -*- coding: utf-8 -*-
from PyQt5 import QtSql
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, QLineEdit, QComboBox, qApp
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QIcon

from dialog_student import AddStudent
from dialog_book import AddBook
from connector_student import TableStudent
from connector_book import TableBook
from connector_student_book import TableStudentBook
from interface import Connect
from style import Style
from message_box import MessageBox


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.numer_grade_book = None
        self.current_student = None
        self.id_books = None
        self.style = Style()
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
        self.setStyleSheet(self.style.main_window())
        self.showFullScreen()
        self.setWindowIcon(QIcon('logo.png'))

        """Левая сторона окна"""
        # Задаем виджеты
        add_student = QPushButton("Добавить студента")
        add_student.setStyleSheet(self.style.button())
        self.del_student = QPushButton("Удалить студента")
        self.del_student.setStyleSheet(self.style.button())
        label_student = QLabel("Студенты:")
        label_student.setStyleSheet(self.style.label())
        self.combo_squad = QComboBox()
        self.combo_squad.setStyleSheet(self.style.combo_box())
        self.combo_squad.setMinimumSize(100, 30)
        self.combo_course = QComboBox()
        self.combo_course.setStyleSheet(self.style.combo_box())
        self.combo_course.setMinimumSize(100, 30)
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
        exit = QPushButton("Выход")
        lable_book = QLabel("Найти по названию книги: ")
        label_library = QLabel("Библиотека:")
        self.label_books_hand = QLabel("Книги на руках:")
        label_id_book = QLabel("Укажите код книги: ")
        self.line_search_book = QLineEdit()
        self.line_id_book = QLineEdit()
        add_book.setStyleSheet(self.style.button())
        lable_book.setStyleSheet(self.style.label())
        label_library.setStyleSheet(self.style.label())
        exit.setStyleSheet(self.style.button())
        label_id_book.setStyleSheet(self.style.label())
        self.line_search_book.setStyleSheet(self.style.line_edit())
        self.label_books_hand.setStyleSheet(self.style.label())
        self.line_id_book.setStyleSheet(self.style.line_edit())
        self.del_book.setStyleSheet(self.style.button())

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
        h2_box.addWidget(self.label_books_hand, 2)
        h2_box.addWidget(label_id_book)
        h2_box.addWidget(self.line_id_book)

        # Делаем вертикальный макет
        self.v1_box = QVBoxLayout()
        self.v1_box.addLayout(h1_box)
        self.v1_box.addWidget(label_library)
        self.v1_box.addWidget(self.table_book)
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
        add_book.clicked.connect(self.update_add_table_book)
        exit.clicked.connect(qApp.quit)
        self.combo_squad.currentTextChanged.connect(self.update_table)
        self.combo_course.currentTextChanged.connect(self.update_table)
        self.table_student.clicked.connect(self.clicked_row_student)
        self.table_book.clicked.connect(self.clicked_row_book)
        self.table_book.doubleClicked.connect(self.add_record)
        self.table_boh.doubleClicked.connect(self.del_record)
        self.line_search_book.textEdited.connect(self.search_book)
        self.del_student.clicked.connect(self.update_del_table_student)
        self.del_book.clicked.connect(self.update_del_table_book)

    def search_book(self):
        self.table_book.delete()
        self.table_book.search_book(self.line_search_book.text())

    def clicked_row_book(self, r):
        column = 0
        a = Connect()
        self.id_books = a.set_book_student(self.table_book.model().index(r.row(), column).data(),
                                           self.table_book.model().index(r.row(), column + 1).data(),
                                           self.table_book.model().index(r.row(), column + 2).data())[0]

    def del_record(self, r):
        column = 0
        a = Connect()
        numer_grade_book = a.get_numer_grade_book(self.current_student)[0]
        code_book = self.table_boh.model().index(r.row(), column + 1).data()
        a.delete_record(numer_grade_book, code_book)
        self.table_boh.delete()
        self.table_boh.create(numer_grade_book)

    def add_record(self, r):
        column = 0
        a = Connect()
        if self.current_student is None:
            return
        numer_grade_book = a.get_numer_grade_book(self.current_student)[0]
        code_book = self.line_id_book.text()
        if self.current_student is not None:
            if len(code_book) == 6:
                id_book = a.get_id_book(self.table_book.model().index(r.row(), column).data(),
                                        self.table_book.model().index(r.row(), column + 1).data(),
                                        self.table_book.model().index(r.row(), column + 2).data())[0]
                bool_exist = a.get_bool_id_book(code_book, id_book)
                if bool_exist is not None:
                    if a.get_record_free(code_book):
                        a.add_record(numer_grade_book, code_book)
                        self.table_boh.delete()
                        self.table_boh.create(numer_grade_book)
                    else:
                        MessageBox("Данная книга занята!!!")
                else:
                    MessageBox("К этой книге не относится этот экземпляр!!!")
            elif len(code_book) == 0:
                MessageBox("Укажите код книги, которую вы хотите дать студенту!!!")
            else:
                MessageBox("Код книги должен иметь 6 цифр!!!")

        else:
            MessageBox("Укажите студента, которому хотите дать книгу!")

    def clicked_row_student(self, r):
        column = 0
        a = Connect()
        self.numer_grade_book = (a.get_student(self.table_student.model().index(r.row(), column).data(),
                                               self.table_student.model().index(r.row(), column + 1).data(),
                                               self.table_student.model().index(r.row(), column + 2).data())[0])
        self.current_student = self.table_student.model().index(r.row(), column).data()
        self.label_books_hand.setText("Книги на руках: " + self.current_student)
        self.table_boh.delete()
        self.table_boh.create(self.numer_grade_book)

    def update_add_table_student(self):
        AddStudent()
        self.update_table()

    def update_del_table_student(self):
        student = Connect()
        result_del = student.delete_student(self.numer_grade_book)
        if result_del:
            self.update_table()
            self.label_books_hand.setText("Книги на руках: ")
            self.current_student = None
        if self.numer_grade_book is None:
            pass
        if not result_del and self.numer_grade_book is not None:
            MessageBox("У студента на руках есть книги!\nДля удаления студента этих книг быть не должно!!!")

    def update_table(self):
        self.table_student.delete()
        self.table_student.create(
            None if self.combo_squad.currentText() == "Группа" else self.combo_squad.currentText(),
            None if self.combo_course.currentText() == "Курс" else self.combo_course.currentText())

    def update_table_book_student(self):
        self.table_boh.delete()
        self.table_boh.create(self.numer_grade_book)

    def update_add_table_book(self):
        AddBook()
        self.table_book.delete()
        self.table_book.create()

    def update_del_table_book(self):
        student = Connect()
        result_del = student.delete_book(self.id_books)
        print(result_del)
        self.table_book.delete()
        self.table_book.create()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = Main()
    myWidget.show()
    app.exec_()
