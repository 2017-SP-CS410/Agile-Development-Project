import random
from enum     import Enum
from pyassimp import load


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


# An example of the Abstract Factory pattern.
class LoadableObject:
    def __init__(self, filename):
	    self.mesh = load(filename).meshes[0]
	    #pull in N and position X and Y randomly with N
	    n = 10
	    self.x = random.randrange(n) - int(n / 2)
	    self.y = random.randrange(n) - int(n / 2)
	
    
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
