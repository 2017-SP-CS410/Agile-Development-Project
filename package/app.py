import sys
from PyQt5.QtWidgets import QApplication
from package.ui      import MainWindow


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.raise_()
    return app.exec_()
