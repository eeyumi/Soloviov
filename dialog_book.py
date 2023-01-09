# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from interface import Connect
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QMessageBox

class AddBook(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Задали окно
        self.setWindowTitle("Добавить книгу")
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        # Задаем виджеты
        label_name = QLabel("Название:")
        label_author = QLabel("Автор:    ")
        label_type = QLabel("Описание:       ")
        label_release = QLabel("Дата выпуска:")

        self.line_name = QLineEdit()
        self.line_author = QLineEdit()
        self.line_type = QLineEdit()
        self.line_release = QLineEdit()

        cancellation = QPushButton("Отмена")
        save = QPushButton("Сохранить")

        # Задаем длину виджета
        self.line_name.setFixedWidth(400)

        reg_fio = QRegExp("[А-я, ]*")
        validator_fio = QRegExpValidator(reg_fio)
        self.line_author.setValidator(validator_fio)

        # Создаем горизонтальные макеты
        h0_box = QHBoxLayout()
        h0_box.addWidget(label_name)
        h0_box.addWidget(self.line_name)

        h1_box = QHBoxLayout()
        h1_box.addWidget(label_author)
        h1_box.addWidget(self.line_author)

        h2_box = QHBoxLayout()
        h2_box.addWidget(label_type)
        h2_box.addWidget(self.line_type)

        reg_number = QRegExp("[0-9]{4,4}")
        validator_number = QRegExpValidator(reg_number)
        self.line_release.setValidator(validator_number)

        h3_box = QHBoxLayout()
        h3_box.addWidget(label_release)
        h3_box.addWidget(self.line_release)

        h4_box = QHBoxLayout()
        h4_box.addWidget(cancellation)
        h4_box.addWidget(save)

        # Создаем вертикальный макет
        v_box = QVBoxLayout(self)
        v_box.addLayout(h0_box)
        v_box.addLayout(h1_box)
        v_box.addLayout(h2_box)
        v_box.addLayout(h3_box)
        v_box.addLayout(h4_box)

        # Добавляем функционал
        cancellation.clicked.connect(self.accept)

        # Добавляем функционал
        cancellation.clicked.connect(self.accept)
        save.clicked.connect(self.save)

        # Добавляем макет в окно
        self.setLayout(v_box)
        self.exec_()

    def save(self):
        list_error = []
        bool_error = False
        if self.line_name.text() == "":
            list_error.append("Вы не указали название книги!\n")
            bool_error = True
        if self.line_author.text() == "":
            list_error.append("Вы не указали автора!\n")
            bool_error = True
        if self.line_type.text() == "":
            list_error.append("Вы не указали короткое описание (два-три слова)!\n")
            bool_error = True
        if self.line_release.text() == "":
            list_error.append("Вы не указали год выпуска!\n")
            bool_error = True
        if bool_error:
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            text_error = ''.join(list_error)
            msg.setText(text_error[:-1])
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            authors = self.line_author.text().replace(', ', ',').replace(' ,', ',').split(',')
            # print(len(authors))
            for i in range(len(authors)):
                book = Connect()
                book.add_book(self.line_name.text(), authors[i], self.line_type.text(), self.line_release.text())
                self.accept()
