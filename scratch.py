import os

#from controller import GameControllerConsoleView
#game = GameControllerConsoleView()
#game.run()

def replace_char_at_str_index(s, ch, i):
    return s[:i] + ch + s[(i+1):]

def replace_substring_by_index(base_string, replacement_substring, start_index):
    end_index = start_index + len(replacement_substring)
    return base_string[:start_index] + replacement_substring + base_string[(end_index):]

def pad_to_max(string, extra_pad=0):
    s_list = string.split('\n')
    pad_width = max([len(s) for s in s_list]) + extra_pad
    string_padded = "\n".join([s.ljust(pad_width) for s in s_list])
    return string_padded

def concat_by_line(list_of_multiline_strings):
    list_of_strings_by_line = [s.split('\n') for s in list_of_multiline_strings]
    out_list = []
    n = len(list_of_strings_by_line[0])
    for i in range(n):
        line = ''.join([s_list[i] for s_list in list_of_strings_by_line])
        out_list.append(line)
    out_string = "\n".join(out_list)
    return out_string


class Assets(object):
    PERSON = """
  \|||/
6 (o o) 
|  (_) 
--|   |--
  |___| |
  | | | 9
 ( ] [ )
""".strip("\n")

    FLOOR = """
+====================================================+
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
+====================================================+
""".strip("\n")

    FLOOR_FLOOR_THICKNESS = 1

    ELEVATOR = """
______________________________________________________________
|-__________________________________________________________-|
||                                                          ||
||                                                          ||
||                                                          ||
||                                                          ||
||                                                          ||
||                                                          ||
||                                                          ||
|-__________________________________________________________-|
|____________________________________________________________| 
""".strip("\n")

    ELEVATOR_FLOOR_THICKNESS = 2





    @staticmethod
    def render_passenger(id):
        s = Assets.PERSON
        s_list = s.split('\n')
        s_list[3] = replace_char_at_str_index(s_list[3], str(id), 4)
        s = "\n".join(s_list)
        return s

    @staticmethod
    def put_people_in_floor(people):
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
            j = i-start #index people with j, from 0
            floor_by_line[i] = replace_substring_by_index(floor_by_line[i],
                                                          people_by_line[j],
                                                          3)
        floor_with_people = "\n".join(floor_by_line)
        return floor_with_people

    @staticmethod
    def put_people_in_elevator(people):
        """
        :param people: a string of peeps next to each other
        """
        people_by_line = people.split('\n')
        elevator_by_line = Assets.ELEVATOR.split('\n')
        people_height = len(people_by_line)
        start = - (Assets.ELEVATOR_FLOOR_THICKNESS + people_height)
        end = - Assets.ELEVATOR_FLOOR_THICKNESS

        for i in range(start, end):
            j = i-start #index people with j, from 0
            elevator_by_line[i] = replace_substring_by_index(elevator_by_line[i],
                                                          people_by_line[j],
                                                          3)
        elevator_with_people = "\n".join(elevator_by_line)
        return elevator_with_people



    @staticmethod
    def merge_passengers(passengers):
        padded_passengers = [pad_to_max(p, extra_pad=2) for p in passengers]
        merged_passengers = concat_by_line(padded_passengers)
        return merged_passengers



class ConsoleView(object):


    def __init__(self, bellhop_viewer, model_vars):
        #self._bellhop_viewer = bellhop_viewer
        self._num_floors = model_vars['num_floors']
        self._capacity = model_vars['capacity']

    def run(self):
        os.system('clear')
        self.print_game()

    def print_game(self):
        floors = [self.get_floor_with_people() for floor_num in range(self._num_floors)]
        elevator = self.get_elevator_with_people()
        #print(elevator)
        elevator_at_floor = 2
        floors[elevator_at_floor] = concat_by_line([floors[elevator_at_floor], elevator])
        #TODO instead merge floors into one str, then place elevator at correct level so feet are level
        for floor in floors:
            print(floor)


    def get_floor_with_people(self):
        #TODO paramaterize with correct floor
        id_list = [1,2,3]
        people = [Assets.render_passenger(id) for id in id_list]
        merged_people = Assets.merge_passengers(people)
        floor_with_people = Assets.put_people_in_floor(merged_people)
        return floor_with_people

    def get_elevator_with_people(self):
        #TODO
        id_list = [4, 5]
        people = [Assets.render_passenger(id) for id in id_list]
        merged_people = Assets.merge_passengers(people)
        elevator_with_people = Assets.put_people_in_elevator(merged_people)
        return elevator_with_people




model_vars = dict(num_floors=4, capacity=14)
cv = ConsoleView(None, model_vars)
cv.run()