from PyQt5.QtWidgets    import QMainWindow, QStackedWidget
from package.ui.widgets import GameWidget

character = {'x': 0, 'y': 0, 'speed': 1}


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Game name here')
        #self.stacked_widget = QStackedWidget(GameWidget())
        self.setCentralWidget(GameWidget())

    def keyPressEvent(self, qKeyEvent):
        key = qKeyEvent.key()
        if key == ord('w')-32:
            character['y'] += character['speed']
        elif key == ord('a')-32:
            character['x'] -= character['speed']
        elif key == ord('s')-32:
            character['y'] -= character['speed']
        elif key == ord('d')-32:
            character['x'] += character['speed']
        elif key == ord(' ')-32:
            print(' ')
