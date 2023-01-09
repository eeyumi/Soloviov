import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,
    QTableWidgetItem, QDockWidget, QFormLayout,
    QLineEdit, QWidget, QPushButton, QSpinBox,
    QMessageBox, QToolBar, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Employees')
        self.setWindowIcon(QIcon('./assets/usergroup.png'))
        self.setGeometry(100, 100, 600, 400)

        employees = [
            {'First Name': 'John', 'Last Name': 'Doe', 'Age': 25},
            {'First Name': 'Jane', 'Last Name': 'Doe', 'Age': 22},
            {'First Name': 'Alice', 'Last Name': 'Doe', 'Age': 22},
        ]

        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)

        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 50)

        self.table.setHorizontalHeaderLabels(employees[0].keys())
        self.table.setRowCount(len(employees))

        row = 0
        for e in employees:
            self.table.setItem(row, 0, QTableWidgetItem(e['First Name']))
            self.table.setItem(row, 1, QTableWidgetItem(e['Last Name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(e['Age'])))
            row += 1







if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())