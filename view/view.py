import abc

from assets.console_assets import Assets
from model.model import BellhopModelInterface

"""
# controls
# todo THIJS link this with new passenger gen
self._indicators_lit = {key: False for key in range(0, self._num_floors)}

# door
self._elevator_moving = False
"""

class ViewInterface(abc.ABC):

    @abc.abstractmethod
    def paint(self) -> None:
        pass

class PyGameViewTextWriter:

    def __init__(self, screen, pygame_font, font_size):
        self._screen = screen
        self._pygame_font = pygame_font
        self._font_size = font_size

    def write(self, game_text):
        self._render_multi_line(game_text, 0, 0)

    def _render_multi_line(self, text, x, y):
        white = 255, 255, 255
        black = 0, 0, 0
        self._screen.fill(black)
        lines = text.splitlines()
        for i, line in enumerate(lines):
            text_surface = self._pygame_font.render(line, False, white)
            self._screen.blit(text_surface, (x, y + self._font_size * i))


class ConsoleView(ViewInterface):


    def __init__(self, bellhop_model: BellhopModelInterface, model_vars, writer):
        self._bellhop_model = bellhop_model
        self._num_floors = model_vars['num_floors']
        self._capacity = model_vars['capacity']
        self._writer = writer

    def paint(self):
        self.print_game()

    def print_game(self):
        floors = [self.get_floor_with_people(floor_num) for floor_num in (range(self._num_floors))]
        elevator = self.get_elevator_with_people()
        elevator_at_floor = self._bellhop_model.get_current_floor()
        floors[elevator_at_floor] = self._concat_by_line([floors[elevator_at_floor], elevator])
        #TODO instead merge floors into one str, then place elevator at correct level so feet are level
        game_text = '\n'.join(reversed(floors))
        self._writer.write(game_text)


    def get_floor_with_people(self, floor_num):
        passengers = self._bellhop_model.get_people_waiting().get(floor_num, [])
        if len(passengers) == 0:
            return Assets.FLOOR
        destination_list = [p._desired_floor for p in passengers]
        people = [self._render_passenger(dest) for dest in destination_list]
        merged_people = self._merge_passengers(people)
        floor_with_people = self._put_people_in_floor(merged_people)
        return floor_with_people

    def get_elevator_with_people(self):
        passengers = self._bellhop_model.get_elevator_contents()
        if len(passengers) == 0:
            return Assets.ELEVATOR
        destination_list = [p._desired_floor for p in passengers]
        people = [self._render_passenger(dest) for dest in destination_list]
        merged_people = self._merge_passengers(people)
        elevator_with_people = self._put_people_in_elevator(merged_people)
        return elevator_with_people

    def _render_passenger(self, id):
        s = Assets.PERSON
        s_list = s.split('\n')
        s_list[3] = self._replace_char_at_str_index(s_list[3], str(id), 4)
        s = "\n".join(s_list)
        return s

    def _put_people_in_floor(self, people):
        """
        :param people: a string of peeps next to each other
        """
        people_by_line = people.split('\n')
        floor_by_line = Assets.FLOOR.split('\n')
        max_shoulder_width = max([len(s) for s in people_by_line])
        people_height = len(people_by_line)
        start = - (Assets.FLOOR_FLOOR_THICKNESS + people_height)
        end = - Assets.FLOOR_FLOOR_THICKNESS

        for i in range(start, end):
            j = i - start  # index people with j, from 0
            floor_by_line[i] = self._replace_substring_by_index(floor_by_line[i],
                                                          people_by_line[j],
                                                          3)
        floor_with_people = "\n".join(floor_by_line)
        return floor_with_people

    def _put_people_in_elevator(self, people):
        """
        :param people: a string of peeps next to each other
        """
        people_by_line = people.split('\n')
        elevator_by_line = Assets.ELEVATOR.split('\n')
        people_height = len(people_by_line)
        start = - (Assets.ELEVATOR_FLOOR_THICKNESS + people_height)
        end = - Assets.ELEVATOR_FLOOR_THICKNESS

        for i in range(start, end):
            j = i - start  # index people with j, from 0
            elevator_by_line[i] = self._replace_substring_by_index(elevator_by_line[i],
                                                             people_by_line[j],
                                                             3)
        elevator_with_people = "\n".join(elevator_by_line)
        return elevator_with_people

    def _merge_passengers(self, passengers):
        padded_passengers = [self._pad_to_max(p, extra_pad=2) for p in passengers]
        merged_passengers = self._concat_by_line(padded_passengers)
        return merged_passengers

    def _replace_char_at_str_index(self, s, ch, i):
        return s[:i] + ch + s[(i + 1):]

    def _replace_substring_by_index(self, base_string, replacement_substring, start_index):
        end_index = start_index + len(replacement_substring)
        return base_string[:start_index] + replacement_substring + base_string[(end_index):]

    def _pad_to_max(self, string, extra_pad=0):
        s_list = string.split('\n')
        pad_width = max([len(s) for s in s_list]) + extra_pad
        string_padded = "\n".join([s.ljust(pad_width) for s in s_list])
        return string_padded

    def _concat_by_line(self, list_of_multiline_strings):
        list_of_strings_by_line = [s.split('\n') for s in list_of_multiline_strings]
        out_list = []
        n = len(list_of_strings_by_line[0])
        for i in range(n):
            line = ''.join([s_list[i] for s_list in list_of_strings_by_line])
            out_list.append(line)
        out_string = "\n".join(out_list)
        return out_string

