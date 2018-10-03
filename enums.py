from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1


class State(Enum):
    ARRIVING = 0
    PEOPLE_OFF = 1
    PEOPLE_ON = 2
    WAIT_INPUT = 3
    MOVING = 4
    LEVEL_COMPLETE = 5
