from enum import Enum
import time

class Direction(Enum):
    UP = 0
    DOWN = 1

class State(Enum):
    ARRIVING = 0
    PEOPLE_OFF = 1
    PEOPLE_ON = 2
    WAIT_INPUT = 3
    MOVING = 4

STATE_TIME_ARRIVAL_SECONDS = 0.5
STATE_TIME_MOVING_SECONDS = 2

# todo MAX how does user input look?
# todo MAX is this sanitized?
class UserInput:
    def __init__(self):
        self._button = ''

    def get_direction(self):
        return Direction.UP


class Bellhop:

    def __init__(self, num_floors, capacity):
        self._curr_state = State.WAIT_INPUT
        self._next_state = State.WAIT_INPUT
        self._state_arrived = time.time() # todo THIJS remove if unused
        self._state_leave = time.time() + float('inf')
        self._input = None

        # floors
        self._num_floors = num_floors
        self._curr_floor = 0

        # controls
        self._buttons_pressed = {}
        self._indicators_lit = {}

        # door
        self._elevator_moving = False

        # people
        self._passenger = []
        self._capacity = capacity

    def step(self):
        if self._curr_state == State.ARRIVING:
            self._setup_next_state(State.PEOPLE_OFF, STATE_TIME_ARRIVAL_SECONDS)
            if self._state_timeout():
                self._goto_next_state()
        elif self._curr_state == State.PEOPLE_OFF:
            pass
        elif self._curr_state == State.PEOPLE_ON:
            pass
        elif self._curr_state == State.WAIT_INPUT:
            if self._input != None:
                self._direction = self._input.get_direction()
                self._goto_next_state()
        elif self._curr_state == State.MOVING:
            self._setup_next_state(State.ARRIVING, STATE_TIME_MOVING_SECONDS)
            if self._state_timeout():
                self._goto_next_state()
        else:
            raise NotImplementedError

    def _setup_next_state(self, next_state, timeout=0.):
        if self._curr_state == self._next_state:
            self._next_state = next_state
            self._state_leave = time.time() + timeout

    def on_input(self):
        pass

    def _state_timeout(self):
        return self._curr_state != self._next_state and self._state_leave > time.time()

    def _goto_next_state(self):
        self._curr_state = self._next_state


class Passenger:
    def __init__(self, floor_entered, desired_floor):
        self._floor_entered = floor_entered
        self._desired_floor = desired_floor

        self._in_elevator = False
        self._dropped_off = False

    def get_desired_floor(self):
        return self._desired_floor


