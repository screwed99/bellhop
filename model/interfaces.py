import abc
from typing import List, Dict, Optional

from enums import State, Direction
from model.passenger import Passenger


class IBellhopView(abc.ABC):

    @abc.abstractmethod
    def get_state(self) -> State:
        pass

    @abc.abstractmethod
    def get_elevator_contents(self) -> List[Passenger]:
        pass

    @abc.abstractmethod
    def get_people_waiting(self) -> Dict[int, List[Passenger]]:
        pass

    @abc.abstractmethod
    def get_current_floor(self) -> int:
        pass


class IBellhopController(abc.ABC):

    @abc.abstractmethod
    def step(self, user_input: Optional[Direction]) -> None:
        pass

    @abc.abstractmethod
    def get_state(self) -> State:
        pass