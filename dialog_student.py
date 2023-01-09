from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from interface import Connect


class AddStudent(QDialog):
    def __init__(self):
        super().__init__()
        self.text_group = "ПМФ"
        self.text_course = "1"
        self.initUI()

    def initUI(self):
        # Задали окно
        self.setWindowTitle("Добавить студента")
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        # Задаем виджеты
        label_surname = QLabel("Фамилия: ")
        label_name = QLabel("Имя:        ")
        label_patronymic = QLabel("Отчество:")
        label_group = QLabel("Группа:")
        label_course = QLabel("Курс:")
        label_number = QLabel("Номер зачетной книжки:")

        self.line_surname = QLineEdit()
        self.line_name = QLineEdit()
        self.line_patronymic = QLineEdit()
        self.line_number = QLineEdit()

        self.list_group = QComboBox()
        self.list_course = QComboBox()

        cancellation = QPushButton("Отмена")
        save = QPushButton("Сохранить")

        # Создаем горизонтальные макеты
        h0_box = QHBoxLayout()
        h0_box.addWidget(label_surname)
        h0_box.addWidget(self.line_surname)

        h1_box = QHBoxLayout()
        h1_box.addWidget(label_name)
        h1_box.addWidget(self.line_name)

        h2_box = QHBoxLayout()
        h2_box.addWidget(label_patronymic)
        h2_box.addWidget(self.line_patronymic)

        h3_box = QHBoxLayout()
        h3_box.addWidget(label_group)
        h3_box.addWidget(self.list_group)
        h3_box.addWidget(label_course)
        h3_box.addWidget(self.list_course)
        h3_box.addWidget(label_number)
        h3_box.addWidget(self.line_number)
        h4_box = QHBoxLayout()
        h4_box.addWidget(cancellation)
        h4_box.addWidget(save)

        # Создаем вертикальный макет
        v_box = QVBoxLayout()
        v_box.addLayout(h0_box)
        v_box.addLayout(h1_box)
        v_box.addLayout(h2_box)
        v_box.addLayout(h3_box)
        v_box.addLayout(h4_box)

        # Добавляем элементы в списки
        self.list_group.addItems(["ПМФ", "БЭК", "ПМ", "АВТ", "ЦТ", "ИТ", "ВТ", "ТМ", "ДП", "ЭП"])
        self.list_course.addItems(["1", "2", "3", "4"])

        # Задаем ввод для зачетки
        reg_number = QRegExp("[0-9]{7,7}")
        validator_number = QRegExpValidator(reg_number)
        self.line_number.setValidator(validator_number)

        # Задаем ввод для ФИО
        reg_fio = QRegExp("[А-я]*")
        validator_fio = QRegExpValidator(reg_fio)
        self.line_name.setValidator(validator_fio)
        self.line_surname.setValidator(validator_fio)
        self.line_patronymic.setValidator(validator_fio)

        # Добавляем функционал
        cancellation.clicked.connect(self.accept)
        self.list_group.currentTextChanged.connect(self.current_text_group)
        self.list_course.currentTextChanged.connect(self.current_text_course)
        save.clicked.connect(self.save)

        # Добавляем макет в окно
        self.setLayout(v_box)
        self.exec_()

    def current_text_group(self, text):
        self.text_group = text

    def current_text_course(self, text):
        self.text_course = text

    def save(self):
        list_error = []
        bool_error = False
        if self.line_number.text() == "":
            list_error.append("Вы не указали номер зачетной книжки!\n")
            bool_error = True
        if self.line_surname.text() == "":
            list_error.append("Вы не указали фамилию студента!\n")
            bool_error = True
        if self.line_name.text() == "":
            list_error.append("Вы не указали имя студента!\n")
            bool_error = True
        if self.line_patronymic.text() == "":
            list_error.append("Вы не указали отчество студента!\n")
            bool_error = True
        if bool_error:
            msg = QMessageBox()
            msg.setWindowTitle("Внимание!")
            text_error = ''.join(list_error)
            msg.setText(text_error[:-1])
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            student = Connect()
            student.add_student(self.line_number.text(), self.line_surname.text()+" "+self.line_name.text()+" "+self.line_patronymic.text(), self.text_group, self.text_course)
            self.accept()



