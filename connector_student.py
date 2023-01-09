from PyQt5 import QtSql
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class TableStudent(QTableWidget):
    def __init__(self):
        super().__init__()
        self.clear()
        query = QtSql.QSqlQuery("""SELECT fullname, squad, course FROM students""")
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["ФИО", "Группа", "Курс"])
        while query.next():
            rows = self.rowCount()
            self.setRowCount(rows + 1)
            self.setItem(rows, 0, QTableWidgetItem(query.value(0)))
            self.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            self.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
        self.resizeColumnsToContents()
        self.setFixedWidth(442)
