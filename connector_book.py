from PyQt5 import QtSql
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class TableBook(QTableWidget):
    def __init__(self):
        super().__init__()
        query = QtSql.QSqlQuery("""SELECT title, release, type_book FROM books""")
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Название книги", "Дата выпуска", "Тип книги"])
        while query.next():
            rows = self.rowCount()
            self.setRowCount(rows + 1)
            self.setItem(rows, 0, QTableWidgetItem(query.value(0)))
            self.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            self.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
        self.resizeColumnsToContents()
        self.setFixedWidth(1400)
