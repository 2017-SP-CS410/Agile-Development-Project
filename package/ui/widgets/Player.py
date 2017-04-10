from enum import Enum


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 1
        self.move = self.Movement.none
        self.rotate = self.Rotate.none
        self.state = self.State.moving

    class Movement(Enum):
        forward = 0
        backward = 1
        none = 2

    class Rotate(Enum):
        clockwise = 0
        counterclockwise = 1
        none = 2

    class State(Enum):
        moving = 0
        typing = 1
