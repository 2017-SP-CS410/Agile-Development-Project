from PyQt5.QtWidgets    import QMainWindow, QStackedWidget
from package.ui.widgets import GameWidget
from enum import Enum


class State(Enum):
    walk = 1
    type = 2

character = {'x': 0, 'y': 0, 'speed': 1, 'state': State.walk}


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

        elif key == ord('ap')-32:
            character['x'] -= character['speed']

        elif key == ord('s')-32:
            character['y'] -= character['speed']

        elif key == ord('d')-32:
            character['x'] += character['speed']

        elif key == ord(' ')-32:
            if character['state'] == State.walk:
                character['state'] == State.type

            elif character['state'] == State.type:
                character['state'] == State.walk
