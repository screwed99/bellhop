from typing import Optional, List, Dict


class Level(object):

    def __init__(self, events, level, num_floors, capacity, length_in_moves) -> None:
        self._events: Dict = events
        self._level_name: str = level
        self._num_floors: int = num_floors
        self._capacity: int = capacity
        self._level_finish_move_number: int = length_in_moves

    def get_num_floors(self) -> int:
        return self._num_floors

    def get_capacity(self) -> int:
        return self._capacity

    def get_event(self, move: int) -> Optional[Dict[int, List[int]]]:
        return self._events.get(move)

    def get_level_finish_move_number(self) -> int:
        return self._level_finish_move_number

    def get_level_name(self) -> str:
        return self._level_name

    def __str__(self):
        return "Level: {} Floors: {} Move #: {}\n" \
               "--Events--:\n{}" \
               "".format(self._level_name,
                         self._num_floors,
                         self._capacity,
                         self._level_finish_move_number,
                         self._events)
