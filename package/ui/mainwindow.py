from PyQt5.QtWidgets    import QMainWindow, QStackedWidget
from package.ui.widgets import GameWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Game name here')
        self.stacked_widget = QStackedWidget(GameWidget())
