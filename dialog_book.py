# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
from PyQt5 import QtCore


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

        line_name = QLineEdit()
        line_author = QLineEdit()
        line_type = QLineEdit()

        cancellation = QPushButton("Отмена")
        save = QPushButton("Сохранить")

        # Задаем длину виджета
        line_name.setFixedWidth(400)

        # Создаем горизонтальные макеты
        h0_box = QHBoxLayout()
        h0_box.addWidget(label_name)
        h0_box.addWidget(line_name)

        h1_box = QHBoxLayout()
        h1_box.addWidget(label_author)
        h1_box.addWidget(line_author)

        h2_box = QHBoxLayout()
        h2_box.addWidget(label_type)
        h2_box.addWidget(line_type)

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

        # Добавляем макет в окно
        self.setLayout(v_box)
        self.exec_()
