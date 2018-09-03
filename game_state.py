

class State:

    def __init__(self):
        # floors
        self._curr_floor = 0
        self._floor_waiting = {}

        # controls
        self._buttons_pressed = {}
        self._indicators_lit = {}

        # door
        self._elevator_moving = False

        # people
        self._passenger = []





class Passenger:
    def __init__(self, floor_entered, desired_floor):
        self._floor_entered = floor_entered
        self._desired_floor = desired_floor

        self._in_elevator = False
        self._dropped_off = False


