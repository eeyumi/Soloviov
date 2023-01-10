# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QIcon
from interface import Connect
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QMessageBox, QCheckBox
from style import Style

class AddBook(QDialog):
    def __init__(self):
        super().__init__()
        self.style = Style()
        self.initUI()

    def initUI(self):
        # Задали окно
        self.setWindowTitle("Добавить книгу")
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setStyleSheet(self.style.main_window())
        self.setWindowIcon(QIcon('logo.png'))

        # Задаем виджеты
        label_name = QLabel("Название:\t")
        label_name.setStyleSheet(self.style.label())
        label_author = QLabel("Автор:\t\t")
        label_author.setStyleSheet(self.style.label())
        label_type = QLabel("Описание:\t")
        label_type.setStyleSheet(self.style.label())
        label_release = QLabel("Дата выпуска:\t")
        label_release.setStyleSheet(self.style.label())
        label_count = QLabel("Кол-во экземпляров:\t")
        label_count.setStyleSheet(self.style.label())

        self.line_name = QLineEdit()
        self.line_name.setStyleSheet(self.style.line_edit1())
        self.line_author = QLineEdit()
        self.line_author.setStyleSheet(self.style.line_edit1())
        self.line_type = QLineEdit()
        self.line_type.setStyleSheet(self.style.line_edit1())
        self.line_release = QLineEdit()
        self.line_release.setStyleSheet(self.style.line_edit1())
        self.line_count = QLineEdit()
        self.line_count.setStyleSheet(self.style.line_edit1())

        self.check_release = QCheckBox("Без даты")
        self.check_release.setStyleSheet(self.style.check_box())
        self.check_author = QCheckBox("Без автора")
        self.check_author.setStyleSheet(self.style.check_box())

        self.check_release.stateChanged.connect(self._stateChanged_slot_release)
        self.check_author.stateChanged.connect(self._stateChanged_slot_author)

        cancellation = QPushButton("Отмена")
        cancellation.setStyleSheet(self.style.button())
        save = QPushButton("Сохранить")
        save.setStyleSheet(self.style.button())

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
        h1_box.addWidget(self.check_author)

        h2_box = QHBoxLayout()
        h2_box.addWidget(label_type)
        h2_box.addWidget(self.line_type)

        reg_number = QRegExp("[0-9]{4,4}")
        validator_number = QRegExpValidator(reg_number)
        self.line_release.setValidator(validator_number)

        reg_count = QRegExp("[0-9]{1,3}")
        validator_number = QRegExpValidator(reg_count)
        self.line_count.setValidator(validator_number)

        h3_box = QHBoxLayout()
        h3_box.addWidget(label_release)
        h3_box.addWidget(self.line_release)
        h3_box.addWidget(self.check_release)

        h4_box = QHBoxLayout()
        h4_box.addWidget(label_count)
        h4_box.addWidget(self.line_count)

        h5_box = QHBoxLayout()
        h5_box.addWidget(cancellation)
        h5_box.addWidget(save)

        # Создаем вертикальный макет
        v_box = QVBoxLayout(self)
        v_box.addLayout(h0_box)
        v_box.addLayout(h1_box)
        v_box.addLayout(h2_box)
        v_box.addLayout(h3_box)
        v_box.addLayout(h4_box)
        v_box.addLayout(h5_box)

        # Добавляем функционал
        cancellation.clicked.connect(self.accept)

        # Добавляем функционал
        cancellation.clicked.connect(self.accept)
        save.clicked.connect(self.save)

        # Добавляем макет в окно
        self.setLayout(v_box)
        self.exec_()

    def _stateChanged_slot_release(self):
        self.line_release.setReadOnly(not self.line_release.isReadOnly())
        self.line_release.setText("")

    def _stateChanged_slot_author(self):
        self.line_author.setReadOnly(not self.line_author.isReadOnly())
        self.line_author.setText("")

    def save(self):
        list_error = []
        bool_error = False
        if self.line_name.text() == "":
            list_error.append("Вы не указали название книги!\n")
            bool_error = True
        if self.line_author.text() == "" and not self.check_author.isChecked():
            list_error.append("Вы не указали автора!\n")
            bool_error = True
        if self.line_type.text() == "":
            list_error.append("Вы не указали короткое описание (два-три слова)!\n")
            bool_error = True
        if self.line_release.text() == "" and not self.check_release.isChecked():
            list_error.append("Вы не указали год выпуска!\n")
            bool_error = True
        if self.line_count.text() == "":
            list_error.append("Вы не указали кол-во экземпляров!\n")
            bool_error = True
        if bool_error:
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            text_error = ''.join(list_error)
            msg.setText(text_error[:-1])
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            if self.check_author.isChecked():
                authors = ["Без автора"]
                print(authors)
            else:
                authors = self.line_author.text().replace(', ', ',').replace(' ,', ',').split(',')
            if self.check_release.isChecked():
                self.line_release.setText("0000")
            for i in range(len(authors)):
                book = Connect()
                book.add_book(self.line_name.text(), authors[i], self.line_type.text(), self.line_release.text())
                book.add_itam_book(self.line_count.text(), self.line_name.text(), self.line_release.text())
                self.accept()
