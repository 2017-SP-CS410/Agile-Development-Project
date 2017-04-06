from textwrap       import dedent
from OpenGL.GL      import *
from OpenGL.GLU     import *
from PyQt5.QtOpenGL import QGLWidget
import math


def setCounts(word):
    vowelCount = 0
    constCount = 0
    #add length over 4


    for char in word:


        if char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u':  # / or use ascii values in array?

            vowelCount += 1

        else:

            constCount += 1


    return {'vowelCount': vowelCount, 'constCount': constCount}


def setPointValue(word):
    wordLen = len(word)
    dif = 0
    result = setCounts(word)
    if wordLen > 4:
        dif = wordLen-4

    pointValue = math.floor(((result['vowelCount'] / result['constCount'])) * 10)

    return pointValue + dif


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
<<<<<<< HEAD
word = "agile"
result = (setCounts(word))
print("Word Value = " + repr(setPointValue(word)) + " vowelCount: "  + repr(result['vowelCount']))

print("why aren't you working!")

=======

    scrabbleVals = {'a': 1, 'b': 3,'c': 3,'d': 2,'e': 1,'f': 4,'g': 2,'h': 4,'i': 1,'j': 8,'k': 5,'l': 1,'m': 3,'n': 1,
                    'o': 1,'p': 3,'q': 10,'r': 1,'s': 1,'t': 1,'u': 1,'v': 4,'w': 4,'x': 8,'y': 4,'z': 10}

    def getLetterValue(word):
        count = 0
        for char in word:

            for letter in GameWidget.scrabbleVals:

                if char == letter:
                    count += GameWidget.scrabbleVals[letter]

        return count
    def getFinalValue(word):
        wordLength = len(word)
        dif = 0
        result = GameWidget.getLetterValue(word)

        if wordLength > 4:
            dif = wordLength -4

        return result + dif

    word = "bingo"
    print(repr(getLetterValue(word)))
    print(repr(getFinalValue(word)))
>>>>>>> 49471c08c1dfbb6bf24c90b167e480e637f73ce7
