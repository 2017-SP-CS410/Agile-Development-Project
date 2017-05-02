import numpy as np
import random
from array       import array
from ctypes      import c_void_p
from enum        import Enum
from math import pi, cos, sin, inf
from pyassimp    import load
from textwrap    import dedent
from OpenGL.GL   import *
from OpenGL.GLU  import *
from PyQt5.QtGui import QMatrix4x4, QVector4D


class Movement(Enum):
    forward = 0
    backward = 1
    none = 2


class Rotate(Enum):
    left = 0
    right = 1
    none = 2


class State(Enum):
    moving = 0
    typing = 1


class Drawable:

    def __init__(self):
        self.model = QMatrix4x4()
        self.initializeGL()
        self.updatePosition()

    def byteData(self, data):
        return data

    def byteSize(self, data):
        return data.nbytes

    def destroy(self):
        glDeleteBuffers(2, [vertexBuffer, faceBuffer])

    def initializeGL(self):
        # create Vertex Array Object on the GPU
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        # create a buffer on the GPU
        vertexBuffer, faceBuffer = glGenBuffers(2)
        # upload the data to the GPU
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.byteSize(self.vertices),
            self.byteData(self.vertices),
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, faceBuffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            self.byteSize(self.faces),
            self.byteData(self.faces),
            GL_STATIC_DRAW
        )
        # load our vertex and fragment shaders onto the GPU
        self.program = self.loadShaders()
        glUseProgram(self.program)
        # bind buffers to shader attributes
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
        position = glGetAttribLocation(self.program, 'position')
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(
            position,
            3,
            GL_FLOAT,
            GL_FALSE,
            0,
            c_void_p(0)
        )
        self.projectionMatrix = glGetUniformLocation(self.program, 'projection')
        self.modelMatrix = glGetUniformLocation(self.program, 'model')

    def loadShaders(self):
        # create a GL Program Object
        program = glCreateProgram()
        # vertex shader
        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, self.vs_source)
        glCompileShader(vs)
        glAttachShader(program, vs)
        if glGetShaderiv(vs, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(vs))
        # fragment shader
        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, self.fs_source)
        glCompileShader(fs)
        glAttachShader(program, fs)
        if glGetShaderiv(fs, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(fs))
        # use the program
        glLinkProgram(program)
        glUseProgram(program)

        return program

    def numFaces(self, faces):
        return sum(map(len, [f for f in faces]))

    def render(self):
        glUseProgram(self.program)
        glBindVertexArray(self.vao)
        glDrawElements(
            self.elements,
            self.numFaces(self.faces),
            GL_UNSIGNED_INT,
            c_void_p(0)
        )

    def loadModelMatrix(self):
        self.updatePosition()
        glUseProgram(self.program)
        glUniformMatrix4fv(
            self.modelMatrix,
            1,
            GL_FALSE,
            array('f', self.model.data()).tostring()
        )

    def resize(self, projection):
        glUseProgram(self.program)
        glUniformMatrix4fv(
            self.projectionMatrix,
            1,
            GL_FALSE,
            array('f', projection.data()).tostring()
        )
        self.loadModelMatrix()

    def updatePosition(self):
        self.position = (self.model * QVector4D(0, 0, 0, 1)).toVector3D()


class Ground(Drawable):

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
    fs_source = dedent("""
        #version 330
        in vec3 fcolor;
        void main()
        {
           gl_FragColor = vec4(fcolor, 1.0);
        }\
    """)

    def __init__(self, n, restart):
        self.elements = GL_TRIANGLE_FAN
        self.generateData(n, restart)
        super(Ground, self).__init__()

    def byteData(self, data):
        return data.tostring()

    def byteSize(self, a):
        return a.itemsize * len(a)

    def generateData(self, n, restart):
        self.vertices = array('f')
        self.colors = array('f')
        self.faces = array('I')
        half_n = n / 2
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
                self.faces.extend([
                     i+0,  i+1,  i+2,  i+3, restart,
                     i+4,  i+5,  i+6,  i+7, restart,
                     i+8,  i+9, i+10, i+11, restart,
                    i+12, i+13, i+14, i+15, restart,
                    i+16, i+17, i+18, i+19, restart,
                    i+20, i+21, i+22, i+23, restart
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
                y += 1
                i += 24
            y = -half_n
            x += 1
        self.faces.pop()

    def initializeGL(self):
        super(Ground, self).initializeGL()
        colorBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, colorBuffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.byteSize(self.colors),
            self.byteData(self.colors),
            GL_STATIC_DRAW
        )
        glBindBuffer(GL_ARRAY_BUFFER, colorBuffer)
        color = glGetAttribLocation(self.program, 'color')
        glEnableVertexAttribArray(color)
        glVertexAttribPointer(
            color,
            3,
            GL_FLOAT,
            GL_FALSE,
            0,
            c_void_p(0)
        )

    def numFaces(self, faces):
        return len(faces)


class LoadableObject(Drawable):

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
    fs_source = dedent("""
        #version 330
        void main()
        {
           gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
        }\
    """)

    def __init__(self, filename, x=0, y=0, direction=0):
        self.elements = GL_TRIANGLES
        self.loadObject(filename)
        super(LoadableObject, self).__init__()
        self.model.rotate(90, 1, 0, 0)
        self.model.translate(x, 0.5, y)
        self.model.rotate(direction, 0, 1, 0)

    def loadObject(self, filename, heightoff=False):
        mesh = load(filename).meshes[0]
        self.vertices = mesh.vertices
        min_x = inf
        max_x = -inf
        min_z = inf
        max_z = -inf
        min_y = 0 if heightoff else inf
        max_y = 0 if heightoff else -inf
        for x, y, z in self.vertices:
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_z = min(z, min_z)
            max_z = max(z, max_z)
            if not heightoff:
                min_y = min(y, min_y)
                max_y = max(y, max_y)
        diff = max(max_x-min_x, max_y-min_y, max_z-min_z)
        for v in self.vertices:
            v /= (diff/2)

        self.faces = mesh.faces
	
    
class TypeableObject(LoadableObject):
    def __init__(self, filename, x, y, direction):
	    super(TypeableObject, self).__init__(filename, x, y, direction)
	    # TODO: get word and score from word bank
	
    def destroy(self):
	    pass
	    # TODO: play destroy sound
	    # TODO: remove from world
	
    
class Cow(TypeableObject):
    def __init__(self, x, y, direction):
        model = 'package/assets/models/cow.obj'
        super(Cow, self).__init__(model, x, y, direction)
	
    
class Bear(TypeableObject):
    def __init__(self, x, y, direction):
        model = 'package/assets/models/bear.obj'
        super(Bear, self).__init__(model, x, y, direction)
	
    
class Giraffe(TypeableObject):
    def __init__(self, x, y, direction):
        model = 'package/assets/models/dirtyGiraffe.obj'
        super(Giraffe, self).__init__(model, x, y, direction)

    def loadObject(self, filename):
	    super(Giraffe, self).loadObject(filename, heightoff=True)
	
	
class Player(LoadableObject):
    def __init__(self):
        super(Player, self).__init__('package/assets/models/player.obj')
        self.dTheta = 6  # degrees
        self.theta = 0
        self.speed = 0.1
        self.movement = Movement.none
        self.rotate = Rotate.none
        self.state = State.moving	

    def move(self):
        if self.state == State.moving:
            if self.movement == Movement.forward:
                self.model.translate(0, 0, self.speed)
            if self.movement == Movement.backward:
                self.model.translate(0, 0, -self.speed)
            if self.rotate == Rotate.left:
                self.theta -= self.dTheta
                self.model.rotate(-self.dTheta, 0, 1, 0)
            elif self.rotate == Rotate.right:
                self.theta += self.dTheta
                self.model.rotate(self.dTheta, 0, 1, 0)
            self.loadModelMatrix()

    def dist(self, o):
        return self.position.distanceToPoint(o.position)


# The Abstract Factory
class Factory:
    def CreateObject(self): pass


# Concrete factories:
class ObjectFactory(Factory):
    _objects = [Cow, Bear, Giraffe]

    def __init__(self, groundsize):
        self.half = groundsize / 2

    def createObject(self):
        x = random.randrange(-self.half, self.half)
        y = random.randrange(-self.half, self.half)
        direction = random.randrange(360)
        return self._objects[random.randrange(len(self._objects))](x, y, direction)

    
    
class PlayerFactory(Factory):
    def createObject(self):
	    return Player()
