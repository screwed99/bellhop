import ast
from levels.level import Level


class LevelParser(object):

    def __init__(self, filename: str='') -> None:
        self._filename: str = filename
        self._parser_last_move_seen: int = -1

    # TODO Add more features
    def parse_from_file(self) -> Level:
        # TODO Add return type to this function
        level_line_seen: bool = False
        events: dict = {}
        level_name: str = ''
        num_floors: int = 0
        capacity: int = 0
        level_finish_move_number: int = 0
        self._parser_last_move_seen: int = -1

        with open(self._filename, 'r') as f:
            for line in f:
                line = line.rstrip()
                if not line or line.startswith('#'):
                    continue

                if line.startswith('level'):
                    level_line_seen = True
                    level_split = line.split(' ')
                    level_name = str(level_split[1])
                    num_floors = int(level_split[2])
                    capacity = int(level_split[3])
                    level_finish_move_number = int(level_split[4])

                elif line.startswith('end_level'):
                    break
                else:
                    self._parse_line(events, line)

        if not level_line_seen:
            raise IOError("Did not see a level line in file {}".format(self._filename))

        level = Level(events, level_name, num_floors, capacity, level_finish_move_number)

        return level

    def _parse_line(self, events: dict, line: str) -> None:

        separator = line.find(':')
        if separator == -1:
            raise IOError("Invalid format in {}, could not find separator(:) on line {}".format(self._filename, line))

        try:
            move = int(line[:separator])
        except ValueError:
            raise IOError("Invalid format in {}, could not parse int from {}".format(self._filename, line[:separator]))

        if move <= self._parser_last_move_seen:
            raise IOError("Invalid format in {}, out of order move {} seen on line {}".format(self._filename, move, line))

        self._parser_last_move_seen = move

        try:
            events[move] = ast.literal_eval(line[separator + 1:])

        except Exception:
            raise IOError("Invalid format in {}, could not parse dict from {}".format(self._filename, line[separator + 1:]))
