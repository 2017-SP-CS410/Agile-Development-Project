import random
from array           import array
from ctypes          import c_void_p
from textwrap        import dedent
from OpenGL.GL       import *
from OpenGL.GLU      import *
from PyQt5.QtCore    import QBasicTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtOpenGL  import QGLWidget
from PyQt5.QtGui     import QImage, QMatrix4x4, QVector3D
from PyQt5.QtWidgets import QProgressBar, QPushButton
from package.ui.widgets.Player import Player


import os



class GameWidget(QGLWidget):



    def __init__(self, n=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(640, 480)
        self.n = n
        self.restart = 0xFFFFFFFF
        self.score = 0
        self.character = Player()

        package_directory = os.path.dirname(os.path.abspath(__file__))
        sfx1 = os.path.join(package_directory, '..','..','assets','sfx','Jump_01.wav')
        self.walk_sfx = QSound(sfx1)
        self.walk_sfx.setLoops(QSound.Infinite)

    def initializeCube(self):

        self.vertices = array('f')
        self.colors = array('f')
        self.indices = array('I')

        half_n = self.n / 2
        x = y = -half_n
        i = 0
        while x < half_n:
            while y < half_n:
                self.vertices.extend([
                    # +y face
                    x+1, y+1,  0,  # 0
                    x+1, y+1, -1,  # 1
                      x, y+1, -1,  # 2
                      x, y+1,  0,  # 3
                    # -y face
                    x+1, y,  0,  # 4
                      x, y,  0,  # 5
                      x, y, -1,  # 6
                    x+1, y, -1,  # 7
                    # top
                    x+1, y+1, 0,  # 8
                      x, y+1, 0,  # 9
                      x,   y, 0,  # 10
                    x+1,   y, 0,  # 11
                    # bottom
                      x,   y, -1,  # 12
                      x, y+1, -1,  # 13
                    x+1, y+1, -1,  # 14
                    x+1,   y, -1,  # 15
                    # +x face
                    x+1,   y,  0,  # 16
                    x+1,   y, -1,  # 17
                    x+1, y+1, -1,  # 18
                    x+1, y+1,  0,  # 19
                    # -x face
                    x,   y,  0,  # 20
                    x, y+1,  0,  # 21
                    x, y+1, -1,  # 22
                    x,   y, -1   # 23
                ])
                self.colors.extend([
                    # top
                    0,1,0,
                    0,1,0,
                    0,1,0,
                    0,1,0,
                    # bottom
                    0,.5,0,
                    0,.5,0,
                    0,.5,0,
                    0,.5,0,
                    # front
                    0,0,1,
                    0,0,1,
                    0,0,1,
                    0,0,1,
                    # back
                    0,0,.5,
                    0,0,.5,
                    0,0,.5,
                    0,0,.5,
                    # right
                    1,0,0,
                    1,0,0,
                    1,0,0,
                    1,0,0,
                    # left
                    .5,0,0,
                    .5,0,0,
                    .5,0,0,
                    .5,0,0
                ])
                self.indices.extend([
                     i+0,  i+1,  i+2,  i+3, self.restart,
                     i+4,  i+5,  i+6,  i+7, self.restart,
                     i+8,  i+9, i+10, i+11, self.restart,
                    i+12, i+13, i+14, i+15, self.restart,
                    i+16, i+17, i+18, i+19, self.restart,
                    i+20, i+21, i+22, i+23, self.restart
                ])
                y += 1
                i += 24
            y = -half_n
            x += 1
        self.indices.pop()

        # create a new Vertex Array Object on the GPU which saves the attribute
        # layout of our vertices
        self.cubeVao = glGenVertexArrays(1)
        glBindVertexArray(self.cubeVao)

        # create a buffer on the GPU for position and color data
        vertexBuffer = glGenBuffers(1)
        colorBuffer = glGenBuffers(1)
        indexBuffer = glGenBuffers(1)

        # upload the data to the GPU, storing it in the buffer we just created
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.sizeof(self.vertices),
            self.vertices.tostring(),
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ARRAY_BUFFER, colorBuffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.sizeof(self.colors),
            self.colors.tostring(),
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBuffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            self.sizeof(self.indices),
            self.indices.tostring(),
            GL_STATIC_DRAW
        )

        # load our vertex and fragment shaders into a program object on the GPU
        program = self.loadShaders()
        glUseProgram(program)
        self.cubeProg = program

        # bind the attribute "position" (defined in our vertex shader) to the
        # currently bound buffer object, which contains our position data
        # this information is stored in our vertex array object
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
        position = glGetAttribLocation(program, 'position')
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
        color = glGetAttribLocation(program, 'color')
        glEnableVertexAttribArray(color)
        glVertexAttribPointer(
            color,
            3,
            GL_FLOAT,
            GL_FALSE,
            0,
            c_void_p(0)
        )

        self.cubeProjMatLoc = glGetUniformLocation(program, "projection")

    def keyPressEvent(self, event):
        key = event.text()
        if key == 'w':
            self.character.move = Player.Movement.forward
            self.walk_sfx.play()
        elif key == 'a':
            self.character.rotate = Player.Rotate.clockwise

        elif key == 's':
            self.character.move = Player.Movement.backward
            self.walk_sfx.play()
        elif key == 'd':
            self.character.rotate = Player.Rotate.counterclockwise

        elif key == ' ':
            if self.character.state == Player.State.moving:
                self.character.move = Player.State.typing

            elif self.character.state == Player.State.typing:
                self.character.move = Player.State.moving

    def keyReleaseEvent(self, event):
        key = event.text()
        if key == 'w':
            self.character.move = Player.Movement.none
            self.walk_sfx.stop()
        elif key == 'a':
            self.character.rotate = Player.Rotate.none

        elif key == 's':
            self.character.move = Player.Movement.none
            self.walk_sfx.stop()
        elif key == 'd':
            self.character.rotate = Player.Rotate.none

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glPrimitiveRestartIndex(self.restart)
        glEnable(GL_PRIMITIVE_RESTART)
        self.initializeCube()
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


    def loadShaders(self):
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

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glDrawArrays(GL_TRIANGLE_FAN, 0, len(self.vertices))
        self.renderCube()

    def renderCube(self):
        glUseProgram(self.cubeProg)
        glBindVertexArray(self.cubeVao)
        glDrawElements(
            GL_TRIANGLE_FAN,
            len(self.indices),
            GL_UNSIGNED_INT,
            c_void_p(0)
        )

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)

        camera = QMatrix4x4()
        camera.perspective(60, 4.0/3.0, 0.1, 100.0)
        camera.lookAt(QVector3D(10, 10, 10), QVector3D(0, 0, 0), QVector3D(0, 0, 1))

        glUseProgram(self.cubeProg)
        glUniformMatrix4fv(
            self.cubeProjMatLoc,
            1,
            GL_FALSE,
            array('f', camera.data()).tostring()
        )

    def sizeof(self, a):
        return a.itemsize * len(a)
