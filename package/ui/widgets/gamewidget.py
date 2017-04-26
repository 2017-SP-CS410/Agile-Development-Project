from array           import array
from collections     import namedtuple
from OpenGL.GL       import *
from OpenGL.GLU      import *
from PyQt5.QtCore    import QBasicTimer
from PyQt5.QtOpenGL  import QGLWidget
from PyQt5.QtGui     import QImage, QMatrix4x4, QVector3D
from PyQt5.QtWidgets import QProgressBar, QPushButton
from .objects        import Ground, Movement, Player, Rotate, State, ObjectFactory


class GameWidget(QGLWidget):

    def __init__(self, num_tiles=20, num_objects=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(640, 480)
        self.num_tiles = num_tiles
        self.num_objects = num_objects
        self.restart = 0xFFFFFFFF
        self.score = 0
        self.objectFactory = ObjectFactory(num_tiles)

    def initializeGround(self):
        self.ground = Ground(self.num_tiles, self.restart)

    def initializeObjects(self):
        self.objects = [self.objectFactory.createObject() for i in range(10)]

    def initializePlayer(self):
        self.player = Player()

    def keyPressEvent(self, event):
        key = event.text()
        if key == 'w':
            self.character.move = Movement.forward

        elif key == 'a':
            self.character.rotate = Rotate.right

        elif key == 's':
            self.character.move = Movement.backward

        elif key == 'd':
            self.character.rotate = Rotate.left

        elif key == ' ':
            if self.character.state == State.moving:
                self.character.move = State.typing

            elif self.character.state == State.typing:
                self.character.move = State.moving

    def keyReleaseEvent(self, event):
        key = event.text()
        if key == 'w':
            self.character.move = Movement.none

        elif key == 'a':
            self.character.rotate = Rotate.none

        elif key == 's':
            self.character.move = Movement.none

        elif key == 'd':
            self.character.rotate = Rotate.none

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glPrimitiveRestartIndex(self.restart)
        glEnable(GL_PRIMITIVE_RESTART)
        # TODO: update each to use objects.py
        self.initializeGround()
        #self.initializePlayer()
        self.initializeObjects()
        self.initializeTimer()
        self.makeScoreLabel()


    def initializeTimer(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.timer = QBasicTimer()
        self.timer.start(1200, self)
        self.step = 100
        self.pbar.setValue(self.step)
        self.btn = QPushButton("Time is: " + str(int(self.step * 1.2)), self)
        self.btn.setStyleSheet("background-color: black; color: red;")
        self.btn.move(500, 10)
        self.show()


    def timerEvent(self, e):
        if self.step <= 0:
            self.timer.stop()
            return
        self.step -= 1
        self.score += 1
        self.btn.setText("Time is: " + str(int(self.step * 1.2)))
        self.scoreLabel.setText("Score: " + str(int(self.score)))
        self.pbar.setValue(self.step)


    def makeScoreLabel(self):
        self.scoreLabel = QPushButton("Score: " + str(int(self.score)), self)
        self.scoreLabel.setStyleSheet("background-color: black; color: red;")
        self.scoreLabel.move(200, 10)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # TODO: render all players and objects
        #self.player.render()
        self.ground.render()
        for o in self.objects:
            o.render()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

        camera = QMatrix4x4()
        camera.perspective(60, 4.0/3.0, 0.1, 100.0)
        camera.lookAt(QVector3D(10, 10, 10), QVector3D(0, 0, 0), QVector3D(0, 0, 10))

        # TODO: resize all players and objects
        #self.player.resize(camera)
        self.ground.resize(camera)
        for o in self.objects:
            o.resize(camera)


scrabbleVals = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
                'M': 3,'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
                'Y': 4, 'Z': 10}

#Calculates the value of each letter then returns the sum
def getLetterValue(word):
    count = 0

    for char in word:
        for letter in scrabbleVals:
            if char == letter:
                count += scrabbleVals[letter]

    return count

#Calulates the final value by evaluating word length
    # then returns the word's letter point value + the word's length point value
def getFinalValue(word):
    wordLength = len(word)
    dif = 0
    letterValue = getLetterValue(word)

    if wordLength > 4:
        dif = wordLength - 4

    return letterValue + dif

#Grabs words from Txt file and calculates final point values
    # then pushes them into a second pre-made Txt file then closes both files
def changeWordFile(self):
    unscored = open("package/assets/words/word_bank_unscored.txt", 'r+')
    scored = open("package/assets/words/word_bank_scored.txt", 'r+')

    for word in unscored:
        pointValue = getFinalValue(word)
        scored.write(word + str(pointValue) + '\n')

    scored.close()
    unscored.close()

changeWordFile("")
