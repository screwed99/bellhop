import ast
from typing import Dict, List

class Level():
    def __init__(self, filename: str='') -> None:
        self._events: Dict[int, List[int]] = {}

        self._level_name = ''
        self._num_floors = 0
        self._total_time_sec = 0.

        if filename != '':
            self.parse_from_file(filename)

    # todo implement interface for getting

    # get_pending_event(time: float) -> Dict[int, List[int]]

    # get_total_time() -> float

    # get_level_name() -> str

    def __str__(self):
        return "Level: {} Floors: {} Time(sec): {}\n" \
               "--Events--:\n{}" \
               "".format(self._level_name, self._num_floors, self._total_time_sec, self._events)

    # todo more features
    def parse_from_file(self, filename: str):
        level_line_seen = False
        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip()
                if not line or line.startswith('##'):
                    continue

                if line.startswith('level'):
                    level_line_seen = True
                    level_split = line.split(' ')
                    self._level_name = str(level_split[1])
                    self._num_floors = int(level_split[2])
                    self._total_time_sec = float(level_split[3])
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
            time = float(line[:separator])
        except ValueError:
            raise IOError("Invalid format in {}, could not parse float from {}".format(filename, line[:separator]))

        if time in self._events.keys():
            raise IOError("Invalid format in {}, timestamp {} seen again on line {}".format(filename, time, line))
        try:
            self._events[time] = ast.literal_eval(line[separator + 1:])

        except:
            raise IOError("Invalid format in {}, could not parse dict from {}".format(filename, line[separator + 1:]))


