# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QComboBox
from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from interface import Connect

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
        label_type = QLabel("Тип:       ")

        self.line_name = QLineEdit()
        self.line_author = QLineEdit()
        self.line_type = QLineEdit()

        cancellation = QPushButton("Отмена")
        save = QPushButton("Сохранить")

        # Задаем длину виджета
        self.line_name.setFixedWidth(400)

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

        h3_box = QHBoxLayout()
        h3_box.addWidget(cancellation)
        h3_box.addWidget(save)

        # Создаем вертикальный макет
        v_box = QVBoxLayout(self)
        v_box.addLayout(h0_box)
        v_box.addLayout(h1_box)
        v_box.addLayout(h2_box)
        v_box.addLayout(h3_box)

        # Добавляем функционал
        cancellation.clicked.connect(self.accept)

        # Добавляем функционал
        cancellation.clicked.connect(self.accept)
        save.clicked.connect(self.save)

        # Добавляем макет в окно
        self.setLayout(v_box)
        self.exec_()

    def current_text_group(self, text):
        self.text_group = text

    def current_text_course(self, text):
        self.text_course = text

    def save(self):
        print("hi")
        book = Connect()
        print(self.line_name.text())
        print(self.line_author.text())
        print(self.line_type.text())
        book.add_book(self.line_name.text(), self.line_author.text(), self.line_type.text())
        self.accept()
