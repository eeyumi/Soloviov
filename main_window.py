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
from interface import Connect
from style import Style



class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.numer_grade_book = None
        self.id_books = None
        self.current_student = None
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
        add_book.setStyleSheet(self.style.button())
        self.del_book = QPushButton("Удалить книгу")
        self.del_book.setStyleSheet(self.style.button())
        lable_book = QLabel("Найти по названию книги: ")
        lable_book.setStyleSheet(self.style.label())
        self.line_search_book = QLineEdit()
        self.line_search_book.setStyleSheet(self.style.line_edit())
        label_library = QLabel("Библиотека:")
        label_library.setStyleSheet(self.style.label())
        self.label_books_hand = QLabel("Книги на руках:")# boh - books on hand (книги на руках) P.s Да-да, с соображалкой у меня туго)))
        self.label_books_hand.setStyleSheet(self.style.label())
        exit = QPushButton("Выход")
        exit.setStyleSheet(self.style.button())
        self.line_id_book = QLineEdit()
        self.line_id_book.setStyleSheet(self.style.line_edit())
        label_id_book = QLabel("Укажите код книги: ")
        label_id_book.setStyleSheet(self.style.label())

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

        h4_box = QHBoxLayout()
        h4_box.addWidget(self.label_books_hand, 2)
        h4_box.addWidget(label_id_book)
        h4_box.addWidget(self.line_id_book)

        # Делаем вертикальный макет
        self.v1_box = QVBoxLayout()
        self.v1_box.addLayout(h1_box)
        self.v1_box.addWidget(label_library)
        self.v1_box.addWidget(self.table_book)
        self.v1_box.addLayout(h4_box)
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
        self.del_student.clicked.connect(lambda: self.update_del_table_student(self.numer_grade_book))
        self.del_book.clicked.connect(self.update_del_table_book)

    def search_book(self):
        self.table_book.delete()
        self.table_book.search_book(self.line_search_book.text())

    def clicked_row_book(self, r):
        column = r.column()
        if column != 0:
            column = 0
        a = Connect()
        self.id_books = a.set_book_student(self.table_book.model().index(r.row(), column).data(),
                                           self.table_book.model().index(r.row(), column + 2).data(),
                                           self.table_book.model().index(r.row(), column + 3).data())[0]

    def del_record(self, r):
        column = r.column()
        if column != 0:
            column = 0
        a = Connect()
        numer_grade_book = a.get_numer_grade_book(self.current_student)[0]
        code_book = self.table_boh.model().index(r.row(), column + 1).data()
        print("\n\n", numer_grade_book)
        print(code_book)
        a.delete_record(numer_grade_book, code_book)
        self.table_boh.delete()
        self.table_boh.create(numer_grade_book)
        print("ошибок нет вроде")



    def add_record(self, r):
        column = r.column()
        if column != 0:
            column = 0
        a = Connect()
        numer_grade_book = a.get_numer_grade_book(self.current_student)[0]
        code_book = self.line_id_book.text()
        if self.current_student is not None:
            if len(code_book) == 6:
                print(code_book)
                # if a.get_bool_id_book(self.line_id_book.text(), ) is not None:
                print("ji")
                id_book = a.get_id_book(self.table_book.model().index(r.row(), column).data(),
                                        self.table_book.model().index(r.row(), column + 2).data(),
                                        self.table_book.model().index(r.row(), column + 3).data())[0]
                print(code_book, "Код книги")
                print(id_book, "ID книги")
                bool_exist = a.get_bool_id_book(code_book, id_book)
                print(bool_exist, " <=====")
                if bool_exist is not None:
                    if a.get_record_free(code_book):
                        a.add_record(numer_grade_book, code_book)
                        print("Можно записать")
                        self.table_boh.delete()
                        self.table_boh.create(numer_grade_book)
                    #
                    # self.id_books = a.set_book_student(self.table_book.model().index(r.row(), column).data(),
                    #                                        self.table_book.model().index(r.row(), column + 1).data(),
                    #                                        self.table_book.model().index(r.row(), column + 2).data())[0]
                    # print("exist")
                    # numer_grade_book =

                    else:
                        msg = QMessageBox()
                        msg.setWindowTitle("Внимание!")
                        msg.setText("Данная книга занята!!!")
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()


                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Внимание!")
                    msg.setText("К этой книге не относится этот экземпляр!!!")
                    msg.setIcon(QMessageBox.Warning)
                    msg.exec_()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Внимание!")
                msg.setText("Укажите код книги, которую вы хотите дать студенту!!!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            msg.setText("Укажите студента, которому хотите дать книгу!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def clicked_row_student(self, r):
        column = r.column()
        if column != 0:
            column = 0
        a = Connect()
        self.numer_grade_book = (a.get_student(self.table_student.model().index(r.row(), column).data(),
                                               self.table_student.model().index(r.row(), column + 1).data(),
                                               self.table_student.model().index(r.row(), column + 2).data())[0])
        print(self.numer_grade_book)
        self.current_student = self.table_student.model().index(r.row(), column).data()
        self.label_books_hand.setText("Книги на руках: " + self.current_student)
        self.table_boh.delete()
        self.table_boh.create(self.numer_grade_book)

    def update_add_table_student(self):
        AddStudent()
        self.update_table()

    def update_del_table_student(self, numer_grade_book):
        student = Connect()
        result_del = student.delete_student(numer_grade_book)
        if result_del:
            self.update_table()
            self.label_books_hand.setText("Книги на руках: ")
        if numer_grade_book is None:
            pass
        if not result_del and numer_grade_book is not None:
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            msg.setText("У студента на руках есть книги!\nДля удаления студента этих книг быть не должно!!!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

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
