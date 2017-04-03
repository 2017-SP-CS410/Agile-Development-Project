from textwrap       import dedent
from OpenGL.GL      import *
from OpenGL.GLU     import *
from PyQt5.QtOpenGL import QGLWidget


class GameWidget(QGLWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumSize(640, 480)


    def initializeGL(self):
        # load our vertex and fragment shaders into a program object on the GPU
        program = self.loadShaders()

        # bind the attribute "position" (defined in our vertex shader) to the
        # currently bound buffer object, which contains our position data
        # this information is stored in our vertex array object
        position = glGetAttribLocation(program, 'position')
        glEnableVertexAttribArray(position)

        # bind the attribute "color" to the buffer object
        color = glGetAttribLocation(program, 'color')
        glEnableVertexAttribArray(color)


    def loadShaders(self):
        # create a GL Program Object
        program = glCreateProgram()

        # vertex shader
        vs_source = dedent("""
            #version 330
            in vec3 position;
            void main()
            {
               gl_Position = vec4(position, 1.0);
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


    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
