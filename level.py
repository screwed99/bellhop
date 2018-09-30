import ast
from typing import Optional, List, Dict


class Level(object):
    """
    move: an int that describes the move number since level start
    event: a dict that describes the passenger generation for a given move, or None
    """

    NULL_EVENT = None  # is making this an explicit variable even neccessary

    def __init__(self, filename: str='') -> None:
        #TODO separate parsing and state
        self._current_event = 0
        self._events = {}
        self._level_name = ''
        self._num_floors = 0
        self._capacity = 0
        self._level_finish_move_number = 0

        if filename != '':
            self.parse_from_file(filename)

    def get_num_floors(self) -> int:
        return self._num_floors

    def get_capacity(self) -> int:
        return self._capacity

    def get_event(self, move: int) -> Optional[Dict[int, List[int]]]:
        return self._events.get(move, self.NULL_EVENT)

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

    # todo more features
    def parse_from_file(self, filename: str):
        level_line_seen = False
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip()
                if not line or line.startswith('#'):
                    continue

                if line.startswith('level'):
                    level_line_seen = True
                    level_split = line.split(' ')
                    self._level_name = str(level_split[1])
                    self._num_floors = int(level_split[2])
                    self._capacity = int(level_split[3])
                    self._level_finish_move_number = int(level_split[4])
                elif line.startswith('end_level'):
                    break
                else:
                    self.parse_line(filename, line)

        if not level_line_seen:
            raise IOError("Did not see a level line in file {}".format(filename))

    def parse_line(self, filename, line):
        separator = line.find(':')
        if separator == -1:
            raise IOError("Invalid format in {}, could not find separator(:) on line {}".format(filename, line))

        try:
            move = int(line[:separator])
        except ValueError:
            raise IOError("Invalid format in {}, could not parse int from {}".format(filename, line[:separator]))

        if move in self._events:
            raise IOError("Invalid format in {}, move {} seen again on line {}".format(filename, move, line))

        try:
            self._events[move] = ast.literal_eval(line[separator + 1:])
        except:
            raise IOError("Invalid format in {}, could not parse dict from {}".format(filename, line[separator + 1:]))


