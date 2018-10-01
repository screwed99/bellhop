import random
import time
from typing import Optional, Dict, List

from enums import State, Direction
from level import Level
from model.gaggle_of_passengers import GaggleOfPassengers
from model.interfaces import IBellhopViewer, IBellhopController
from model.passenger import Passenger

random.seed(time.time())

STATE_TIME_ARRIVAL_SECONDS = 0.5
STATE_TIME_PEOPLE_OFF_SECONDS = 0.5
STATE_TIME_PEOPLE_ON_SECONDS = 0.5
STATE_TIME_MOVING_SECONDS = 2
PASSENGER_PCT_CHANCE_PER_TICK = 0.1


class BellhopModel(IBellhopViewer, IBellhopController):

    def __init__(self, level: Level) -> None:
        self._level = level
        self._curr_state: State = State.ARRIVING
        self._next_state: State = State.ARRIVING
        self._state_leave: float = time.time() + float('inf')
        self._user_input: Optional[Direction] = None
        self._move_count = 0

        # floors
        self._num_floors: int = self._level.get_num_floors()
        self._curr_floor: int = 0

        # people
        self._passengers: GaggleOfPassengers = GaggleOfPassengers()
        self._capacity: int = self._level.get_capacity()

    def get_state(self) -> State:
        return self._curr_state

    def get_elevator_contents(self) -> List[Passenger]:
        return self._passengers.get_passengers_in_elevator()

    def get_people_waiting(self) -> Dict[int, List[Passenger]]:
        return self._passengers.get_passengers_waiting_by_floor()

    def get_current_floor(self) -> int:
        return self._curr_floor

    def step(self, user_input: Optional[Direction]) -> None:
        self._user_input = user_input

        if self._curr_state == State.ARRIVING:
            self._setup_next_state(State.PEOPLE_OFF, STATE_TIME_ARRIVAL_SECONDS)
            if self._state_timeout():
                self._make_passengers_from_schedule()
                self._goto_next_state()

        elif self._curr_state == State.PEOPLE_OFF:
            self._setup_next_state(State.PEOPLE_ON, STATE_TIME_PEOPLE_OFF_SECONDS)
            self._passengers.drop_off(self.get_current_floor())
            if self._state_timeout():
                self._goto_next_state()

        elif self._curr_state == State.PEOPLE_ON:
            #TODO smart passengers that only get on if elevator is heading right direction
            self._setup_next_state(State.WAIT_INPUT, STATE_TIME_PEOPLE_ON_SECONDS)
            qty_to_pick_up = self._get_space_available_in_elevator()
            self._passengers.pick_up(self.get_current_floor(), qty_to_pick_up)
            if self._state_timeout():
                self._goto_next_state()

        elif self._curr_state == State.WAIT_INPUT:
            self._setup_next_state(State.MOVING,
                                   STATE_TIME_PEOPLE_ON_SECONDS)

            if self._user_input is not None:
                self._direction = self._user_input
                self._user_input = None
                if self._change_floor():
                    self._move_count += 1
                    self._goto_next_state()

        elif self._curr_state == State.MOVING:
            self._setup_next_state(State.ARRIVING, STATE_TIME_MOVING_SECONDS)
            if self._state_timeout():
                self._goto_next_state()
        else:
            raise NotImplementedError

    def _setup_next_state(self, next_state: State, timeout: float=0.) -> bool:
        if self._curr_state == self._next_state:
            self._next_state = next_state
            self._state_leave = time.time() + timeout
            return True
        return False

    def _goto_next_state(self) -> None:
        self._curr_state = self._next_state

    def _get_space_available_in_elevator(self) -> int:
        return self._capacity - len(self.get_elevator_contents())

    def _make_random_passenger(self, force: bool=False) -> None:
        #TODO clean up depending on level's needs
        if force or random.random() < PASSENGER_PCT_CHANCE_PER_TICK:
            start_floor = random.randint(0, self._num_floors - 1)
            end_floor = start_floor
            while end_floor == start_floor:
                end_floor = random.randint(0, self._num_floors - 1)
            p = Passenger(start_floor, end_floor)
            self._passengers.add_passenger(p)

    def _make_passengers_from_schedule(self) -> None:
        #TODO support random passenger gen if asked by level
        event = self._level.get_event(self._move_count)
        if event is None:
            return None
        for start_floor in event:
            for end_floor in event[start_floor]:
                p = Passenger(start_floor, end_floor)
                self._passengers.add_passenger(p)

    def _change_floor(self) -> bool:
        if self._direction == Direction.UP and self._curr_floor < self._num_floors - 1:
            self._curr_floor += 1
            return True
        elif self._direction == Direction.DOWN and self._curr_floor > 0:
            self._curr_floor -= 1
            return True
        return False

    def _state_timeout(self) -> bool:
        return self._curr_state != self._next_state and self._state_leave > time.time()

    def _is_game_finished(self) -> bool:
        # TODO use this in controller
        is_level_schedule_complete = self._level.get_level_finish_move_number() <= self._move_count
        are_lobbies_empty = len(self._passengers.get_passengers_waiting_by_floor()) == 0
        is_elevator_empty = len(self.get_elevator_contents()) == 0
        return is_level_schedule_complete and are_lobbies_empty and is_elevator_empty
