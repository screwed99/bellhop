import time
import random
from enums import State, Direction
random.seed(time.time())

STATE_TIME_ARRIVAL_SECONDS = 0.5
STATE_TIME_PEOPLE_OFF_SECONDS = 0.5
STATE_TIME_PEOPLE_ON_SECONDS = 0.5
STATE_TIME_MOVING_SECONDS = 2

PASSENGER_PCT_CHANCE_PER_TICK = 0.1


class Bellhop:
    def __init__(self, num_floors, capacity):
        self._curr_state = State.WAIT_INPUT
        self._next_state = State.WAIT_INPUT
        self._state_leave = time.time() + float('inf')
        self._user_input = None

        # floors
        self._num_floors = num_floors
        self._curr_floor = 0

        # controls
        # todo THIJS link this with new passenger gen
        self._indicators_lit = {key: False for key in range(0, self._num_floors)}

        # door
        self._elevator_moving = False

        # people
        self._passengers = GaggleOfPassengers()
        # todo enforce capacity
        self._capacity = capacity

    def __str__(self):
        ret = "{} ON {} | ".format(self.get_state(), self._curr_floor)
        ret += "\n|----- Elevator -----|\n"
        people_in = self.get_elevator_contents()
        for x in people_in:
            ret += "| {} |\n".format(x)
        ret += "|____________________|\n"
        people_waiting = self.get_people_waiting()
        for x in people_waiting:
            ret += "{}\n".format(x)
            for y in people_waiting[x]:
                ret += "{} ".format(y)
            ret += "\n"
        return ret


    def step(self, user_input):
        self._user_input = user_input

        self.make_random_passenger()
        if self._curr_state == State.ARRIVING:
            self._setup_next_state(State.ARRIVING, State.PEOPLE_OFF, STATE_TIME_ARRIVAL_SECONDS)
            if self._state_timeout():
                # more actions?
                self._goto_next_state()

        elif self._curr_state == State.PEOPLE_OFF:
            self._setup_next_state(State.PEOPLE_OFF, State.PEOPLE_ON, STATE_TIME_PEOPLE_OFF_SECONDS)
            self._passengers.drop_off(self._curr_floor)
            if self._state_timeout():
                self._goto_next_state()

        elif self._curr_state == State.PEOPLE_ON:
            self._setup_next_state(State.PEOPLE_ON, State.WAIT_INPUT, STATE_TIME_PEOPLE_ON_SECONDS)
            self._passengers.pick_up(self._curr_floor)
            if self._state_timeout():
                self._goto_next_state()

        elif self._curr_state == State.WAIT_INPUT:
            changed = self._setup_next_state(State.WAIT_INPUT,
                                             State.MOVING,
                                             STATE_TIME_PEOPLE_ON_SECONDS)
            if changed:
                self.make_random_passenger(force=True)
                print(self) # todo remove this startup hack

            if self._user_input is not None:
                self._direction = self._user_input.get_direction()
                self._user_input = None
                if self._change_floor():
                    self._goto_next_state()

        elif self._curr_state == State.MOVING:
            self._setup_next_state(State.MOVING, State.ARRIVING, STATE_TIME_MOVING_SECONDS)
            if self._state_timeout():
                self._goto_next_state()
        else:
            raise NotImplementedError

    def _setup_next_state(self, in_state, next_state, timeout=0.):
        if self._curr_state == self._next_state:
            self._next_state = next_state
            self._state_leave = time.time() + timeout
            return True
        return False

    def _goto_next_state(self):
        print(self)
        self._curr_state = self._next_state

    def get_state(self):
        return self._curr_state

    def get_elevator_contents(self):
        return self._passengers.get_passengers_in_elevator()

    def get_people_waiting(self):
        return self._passengers.get_passengers_waiting_by_floor()

    def make_random_passenger(self, force=False):
        if force or random.random() < PASSENGER_PCT_CHANCE_PER_TICK:
            start_floor = random.randint(0, self._num_floors - 1)
            end_floor = start_floor
            while end_floor == start_floor:
                end_floor = random.randint(0, self._num_floors - 1)
            p = Passenger(start_floor, end_floor)
            self._passengers.add_passenger(p)

    def _change_floor(self):
        if self._direction == Direction.UP and self._curr_floor < self._num_floors:
            self._curr_floor += 1
            return True
        elif self._direction == Direction.DOWN and self._curr_floor > 0:
            self._curr_floor -= 1
            return True
        return False

    def _state_timeout(self):
        return self._curr_state != self._next_state and self._state_leave > time.time()



class Passenger:
    id_num = 0
    def __init__(self, floor_entered, desired_floor):
        self._floor_entered = floor_entered
        self._desired_floor = desired_floor

# todo THIJS make passenger state enum
        self._in_elevator = False
        self._dropped_off = False
        self._id = Passenger.id_num
        Passenger.id_num += 1  # is this legit?

    def __str__(self):
        return "Pass[id: {} start:{} dest:{} in:{} drop: {}]"\
            .format(self._id,
                    self._floor_entered,
                    self._desired_floor,
                    self._in_elevator,
                    self._dropped_off)

    def get_desired_floor(self):
        return self._desired_floor

    def pick_up(self):
        assert(not self._in_elevator and not self._dropped_off)
        self._in_elevator = True
        print("Picked up passenger ", self._id)

    def drop_off(self):
        assert(self._in_elevator)
        self._in_elevator = False
        self._dropped_off = True
        print("Dropped off passenger ", self._id)

    def is_waiting_for_pickup(self):
        return not self._in_elevator and not self._dropped_off

    def is_in_elevator(self):
        return self._in_elevator

    def is_dropped_off(self):
        return self._dropped_off



class GaggleOfPassengers:
    def __init__(self):
        self._passengers = []

    def add_passenger(self, passenger):
        self._passengers.append(passenger)

    def get_passengers_in_elevator(self):
        return [passenger for passenger in self._passengers if passenger._in_elevator]

    def get_passengers_waiting(self):
        return [passenger for passenger in self._passengers if passenger.is_waiting_for_pickup()]

    def get_passengers_waiting_by_floor(self):
        waiting_by_floor = {}
        for passenger in self.get_passengers_waiting():
            floor = passenger._floor_entered
            if floor not in waiting_by_floor:
                waiting_by_floor[floor] = []
            waiting_by_floor[floor].append(passenger)
        return waiting_by_floor

    def pick_up(self, floor):
        for passenger in self.get_passengers_waiting_by_floor().get(floor, []):
            passenger.pick_up()

    def drop_off(self, floor):
        for passenger in self.get_passengers_in_elevator():
            if passenger._desired_floor == floor:
                passenger.drop_off()
