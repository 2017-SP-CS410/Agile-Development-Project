from array           import array
from collections     import namedtuple
from ctypes          import c_void_p
from textwrap        import dedent
from OpenGL.GL       import *
from OpenGL.GLU      import *
from PyQt5.QtCore    import QBasicTimer
from PyQt5.QtOpenGL  import QGLWidget
from PyQt5.QtGui     import QImage, QMatrix4x4, QVector3D
from PyQt5.QtWidgets import QProgressBar, QPushButton
from .objects        import Ground, Movement, Player, Rotate, State


class GameWidget(QGLWidget):

    def __init__(self, n=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(640, 480)
        self.n = n
        self.restart = 0xFFFFFFFF
        self.score = 0


    def initializeGround(self):

        self.ground = Ground(self.n, self.restart)

        # create a new Vertex Array Object on the GPU which saves the attribute
        # layout of our vertices
        self.groundVao = glGenVertexArrays(1)
        glBindVertexArray(self.groundVao)

        # create a buffer on the GPU for position and color data
        vertexBuffer, colorBuffer, indexBuffer = glGenBuffers(3)

        # upload the data to the GPU, storing it in the buffer we just created
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.sizeof(self.ground.vertices),
            self.ground.vertices.tostring(),
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ARRAY_BUFFER, colorBuffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.sizeof(self.ground.colors),
            self.ground.colors.tostring(),
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBuffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            self.sizeof(self.ground.indices),
            self.ground.indices.tostring(),
            GL_STATIC_DRAW
        )

        # load our vertex and fragment shaders into a program object on the GPU
        self.groundProgram = self.loadGroundShaders()
        glUseProgram(self.groundProgram)

        # bind the attribute "position" (defined in our vertex shader) to the
        # currently bound buffer object, which contains our position data
        # this information is stored in our vertex array object
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
        position = glGetAttribLocation(self.groundProgram, 'position')
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(
            position,
            3,
            GL_FLOAT,
            GL_FALSE,
            0,
            c_void_p(0)
        )
        glBindBuffer(GL_ARRAY_BUFFER, colorBuffer)
        color = glGetAttribLocation(self.groundProgram, 'color')
        glEnableVertexAttribArray(color)
        glVertexAttribPointer(
            color,
            3,
            GL_FLOAT,
            GL_FALSE,
            0,
            c_void_p(0)
        )

        self.groundProjMatLoc = glGetUniformLocation(self.groundProgram, "projection")


    def initializePlayer(self):
        self.player = Player()

        # create a new Vertex Array Object on the GPU which saves the attribute
        # layout of our vertices
        self.playerVao = glGenVertexArrays(1)
        glBindVertexArray(self.playerVao)

        # create a buffer on the GPU for position and color data
        vertexBuffer, faceBuffer = glGenBuffers(2)

        # upload the data to the GPU, storing it in the buffer we just created
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.player.vertices.nbytes,
            self.player.vertices,
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, faceBuffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            self.player.faces.nbytes,
            self.player.faces,
            GL_STATIC_DRAW
        )

        # load our vertex and fragment shaders into a program object on the GPU
        self.playerProgram = self.loadPlayerShaders()
        glUseProgram(self.playerProgram)

        # bind the attribute "position" (defined in our vertex shader) to the
        # currently bound buffer object, which contains our position data
        # this information is stored in our vertex array object
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
        position = glGetAttribLocation(self.playerProgram, 'position')
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(
            position,
            3,
            GL_FLOAT,
            GL_FALSE,
            0,
            c_void_p(0)
        )

        self.playerProjMatLoc = glGetUniformLocation(self.playerProgram, "projection")
        self.modelModelMatLoc = glGetUniformLocation(self.playerProgram, "model")

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
        self.initializeGround()
        self.initializePlayer()
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


    def loadGroundShaders(self):
        # create a GL Program Object
        program = glCreateProgram()

        # vertex shader
        vs_source = dedent("""
            #version 330
            uniform mat4 projection;
            in vec3 position;
            in vec3 color;
            out vec3 fcolor;
            void main()
            {
               gl_Position = projection * vec4(position, 1.0);
               fcolor = color;
            }\
        """)
        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, vs_source)
        glCompileShader(vs)
        glAttachShader(program, vs)
        if glGetShaderiv(vs, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(vs))

        # fragment shader
        fs_source = dedent("""
            #version 330
            in vec3 fcolor;
            void main()
            {
               gl_FragColor = vec4(fcolor, 1.0);
            }\
        """)
        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, fs_source)
        glCompileShader(fs)
        glAttachShader(program, fs)
        if glGetShaderiv(fs, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(fs))

        # use the program
        glLinkProgram(program)
        glUseProgram(program)

        return program


    def loadPlayerShaders(self):
        # create a GL Program Object
        program = glCreateProgram()

        # vertex shader
        vs_source = dedent("""
            #version 330
            uniform mat4 projection;
            uniform mat4 model;
            in vec3 position;
            void main()
            {
               gl_Position = projection * model * vec4(position, 1.0);
            }\
        """)
        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, vs_source)
        glCompileShader(vs)
        glAttachShader(program, vs)
        if glGetShaderiv(vs, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(vs))

        # fragment shader
        fs_source = dedent("""
            #version 330
            void main()
            {
               gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
            }\
        """)
        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, fs_source)
        glCompileShader(fs)
        glAttachShader(program, fs)
        if glGetShaderiv(fs, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(fs))

        # use the program
        glLinkProgram(program)
        glUseProgram(program)

        return program

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.renderGround()
        self.renderPlayer()

    def renderGround(self):
        glUseProgram(self.groundProgram)
        glBindVertexArray(self.groundVao)
        glDrawElements(
            GL_TRIANGLE_FAN,
            len(self.ground.indices),
            GL_UNSIGNED_INT,
            c_void_p(0)
        )

    def renderPlayer(self):
        glUseProgram(self.playerProgram)
        glBindVertexArray(self.playerVao)
        glDrawElements(
            GL_TRIANGLES,
            sum(map(len, [f for f in self.player.faces])),
            GL_UNSIGNED_INT,
            c_void_p(0)
        )

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

        camera = QMatrix4x4()
        camera.perspective(60, 4.0/3.0, 0.1, 100.0)
        camera.lookAt(QVector3D(10, 10, 10), QVector3D(0, 0, 0), QVector3D(0, 0, 10))

        glUseProgram(self.groundProgram)
        glUniformMatrix4fv(
            self.groundProjMatLoc,
            1,
            GL_FALSE,
            array('f', camera.data()).tostring()
        )

        glUseProgram(self.playerProgram)
        glUniformMatrix4fv(
            self.playerProjMatLoc,
            1,
            GL_FALSE,
            array('f', camera.data()).tostring()
        )

        print('player: {0}'.format(self.player.model))
        glUseProgram(self.playerProgram)
        glUniformMatrix4fv(
            self.modelModelMatLoc,
            1,
            GL_FALSE,
            array('f', self.player.model.data()).tostring()
        )

    def sizeof(self, a):
        return a.itemsize * len(a)

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
