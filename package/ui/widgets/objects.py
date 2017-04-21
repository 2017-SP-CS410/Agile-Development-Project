import math
import random
from array       import array
from enum        import Enum
from pyassimp    import load
from PyQt5.QtGui import QMatrix4x4


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

class Ground:
    def __init__(self, n, restart):

        self.vertices = array('f')
        self.colors = array('f')
        self.indices = array('I')

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
                     i+0,  i+1,  i+2,  i+3, restart,
                     i+4,  i+5,  i+6,  i+7, restart,
                     i+8,  i+9, i+10, i+11, restart,
                    i+12, i+13, i+14, i+15, restart,
                    i+16, i+17, i+18, i+19, restart,
                    i+20, i+21, i+22, i+23, restart
                ])
                y += 1
                i += 24
            y = -half_n
            x += 1
        self.indices.pop()


class LoadableObject:
    def __init__(self, filename):
        mesh = load(filename).meshes[0]
        self.vertices = mesh.vertices
        min_x = math.inf
        max_x = -math.inf
        min_y = math.inf
        max_y = -math.inf
        min_z = math.inf
        max_z = -math.inf
        for x, y, z in self.vertices:
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)
            min_z = min(z, min_z)
            max_z = max(z, max_z)
        diff = max(max_x-min_x, max_y-min_y, max_z-min_z)
        for v in self.vertices:
            v /= diff

        self.faces = mesh.faces
        self.model = QMatrix4x4()
        self.model.rotate(90, 1, 0, 0)
        self.model.translate(0, 0.5, 0)
        #pull in N and position X and Y randomly with N
        self.x = 0
        self.y = 0
	
    
class TypeableObject(LoadableObject):
    def __init__(self, filename):
	    super(TypeableObject, self).__init__(filename)
	    # TODO: get word and score from word bank
	
    def destroy(self):
	    pass
	    # TODO: play destroy sound
	    # TODO: remove from world
	
    
class RedBox(TypeableObject):
    def __init__(self):
	    super(RedBox, self).__init__('path/to/red/model')
	
    
class BlueBox(TypeableObject):
    def __init__(self):
	    super(BlueBox, self).__init__('path/to/blue/model')
	
	
class Player(LoadableObject):
    def __init__(self):
        super(Player, self).__init__('package/assets/models/cow.obj')
        self.vx = 0
        self.vy = 0
        self.theta = 0
        self.move = Movement.none
        self.rotate = Rotate.none
        self.state = State.moving	
	
    
# The Abstract Factory
class ObjectFactory:
    def CreateObject(self): pass
	

# Concrete factories:
class BoxFactory(ObjectFactory):
    _boxes = [RedBox, BlueBox]
    def CreateObject(self):
	    return self._boxes[random.randrange(len(self._boxes))]()
    
    
class PlayerFactory(ObjectFactory):
    def CreateObject(self):
	    return Player()
