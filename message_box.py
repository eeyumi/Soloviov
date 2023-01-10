from PyQt5.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Внимание!")
        self.setText(text)
        self.setIcon(QMessageBox.Warning)
        self.exec_()
