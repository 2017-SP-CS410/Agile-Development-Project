from PyQt5.QtGui     import *
from PyQt5.QtOpenGL  import QGLWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from textwrap        import dedent
from PyQt5.QtMultimedia   import QSound
import sys

app = QCoreApplication(sys.argv)

sound = QSound("/home/asher/Agile-Development-Project/package/theme.wav")

sound.setLoops(QSound.Infinite)

sound.play()

app.exec()