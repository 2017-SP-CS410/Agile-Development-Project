import os
from random             import randrange, randint
from OpenGL.GL          import *
from OpenGL.GLU         import *
from PyQt5.QtCore       import QBasicTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtOpenGL     import QGLWidget
from PyQt5.QtGui     import QMatrix4x4, QVector3D
from PyQt5.QtWidgets import QProgressBar, QPushButton, QLineEdit
from .objects        import Ground, Movement, Player, Rotate, State, ObjectFactory
from package.utilities.word import getFinalValue, makeWordList


class GameWidget(QGLWidget):
    #   ********** Destroy sound for typable object ***********
    # sfx_dir = os.path.join(os.path.abspath(__file__))
    # destroy = os.path.join(sound_dir, '..', '..', 'assets', 'SoundEffects', 'destroy.wav')
    # destroySFX = QSound(destroy)
    # destroySFX.play()

    # *********** Success Sound for completed word **************
    # sfx_dir = os.path.join(os.path.abspath(__file__))
    # success = os.path.join(sfx_dir, '..', '..', 'assets', 'SoundEffects', 'destroy.wav')
    # fail =  os.path.join(sfx_dir, '..', '..', 'assets', 'SoundEffects', 'destroy.wav')
    # successSFX = QSound(success)
    # failSFX = QSound(fail)

    def __init__(self, num_tiles=20, num_objects=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(640, 480)
        self.num_tiles = num_tiles
        self.num_objects = num_objects
        self.restart = 0xFFFFFFFF

        package_directory = os.path.dirname(os.path.abspath(__file__))

        music1 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '1.wav')
        music2 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '2.wav')
        music3 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '3.wav')
        music4 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '4.wav')
        music5 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '5.wav')
        music6 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '6.wav')
        music7 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '7.wav')
        music8 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '8.wav')
        music9 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '9.wav')
        music10 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '10.wav')
        music11 = os.path.join(package_directory, '..', '..', 'assets', 'Music', '11.wav')


        songs = [music1, music2, music3, music4, music5, music6, music7, music8, music9, music10, music11]
        randIndex = randrange(0,len(songs))
        randMusic = songs[randIndex]

        self.backgroundMusic = QSound(randMusic)

        self.backgroundMusic.setLoops(QSound.Infinite)
        self.score = 0
        self.objectFactory = ObjectFactory(num_tiles)
        self.wordList = makeWordList()


    def initializeGround(self):
        self.ground = Ground(self.num_tiles, self.restart)

    def initializeObjects(self):
        self.objects = [self.objectFactory.createObject() for i in range(10)]

    def initializePlayer(self):
        self.player = Player()

    def keyPressEvent(self, event):
        key = event.text()
        if key == 'w':
            self.player.move = Movement.forward
        elif key == 'a':
            self.player.rotate = Rotate.right
        elif key == 's':
            self.player.move = Movement.backward
        elif key == 'd':
            self.player.rotate = Rotate.left
        elif key == ' ':
            if self.player.state == State.moving:
                self.player.move = State.typing
            elif self.player.state == State.typing:
                self.player.move = State.moving

    def keyReleaseEvent(self, event):
        key = event.text()
        if key in ['w', 'a', 's', 'd']:
            self.player.move = Movement.none


    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glPrimitiveRestartIndex(self.restart)
        glEnable(GL_PRIMITIVE_RESTART)
        self.initializeGround()
        self.initializePlayer()
        self.initializeObjects()
        self.playMusic()
        self.clockStart()
        self.typeBox()
        self.initializeTimer()
        self.makeScoreLabel()

    def initializeTimer(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setValue(int(self.step/1.2))
        self.btn = QPushButton("Time is: " + str(int(self.step)), self)
        self.btn.setStyleSheet("background-color: black; color: red;")
        self.btn.move(500, 10)
        self.show()

    def timerEvent(self, e):
        if self.step <= 0:
            self.timer.stop()
            return
        self.step -= 1 / 60
        if (self.readbox.text() == self.textbox.text()):
            self.textbox.setText("")
        self.btn.setText("Time is: " + str(int((self.step))))
        self.scoreLabel.setText("Score: " + str(int(self.score)))
        self.pbar.setValue(int(self.step / 1.2))

    def wordCompleted(self, word):
        self.score += getFinalValue(word)
        self.scoreLabel.setText("Score: " + self.score)

    def typeBox(self):
        ran = randint(0, len(self.wordList))
        word = self.wordList[ran]
        value = getFinalValue(word)
        self.readbox = QLineEdit(self)
        self.readbox.setText(word)
        self.readbox.setStyleSheet("background-color: black; color: red; border-color: black;")
        self.readbox.setReadOnly(True)
        self.readbox.move(0, 420)
        self.readbox.resize(640, 30)
        self.textbox = QLineEdit(self)
        self.textbox.setStyleSheet("background-color: black; color: red; border-color: black;")
        self.textbox.move(0, 450)
        self.textbox.setFocus()
        self.textbox.resize(640, 30)

    def clockStart(self):
        self.timer = QBasicTimer()
        self.timer.start(50/3, self)
        self.step = 120

    def makeScoreLabel(self):
        self.scoreLabel = QPushButton("Score: " + str(int(self.score)), self)
        self.scoreLabel.setStyleSheet("background-color: black; color: red;")
        self.scoreLabel.move(200, 10)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.player.render()
        self.ground.render()
        for o in self.objects:
            o.render()

    def playMusic(self):
        self.backgroundMusic.play()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        # create the camera
        camera = QMatrix4x4()
        camera.perspective(60, 4.0/3.0, 0.1, 100.0)
        camera.lookAt(QVector3D(10, 10, 10), QVector3D(0, 0, 0), QVector3D(0, 0, 10))
        # resize all the drawable objects
        self.player.resize(camera)
        self.ground.resize(camera)
        for o in self.objects:
            o.resize(camera)
