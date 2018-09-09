import time

from model import Bellhop
from enums import State, Direction

# todo MAX how does user input look?
# todo MAX is this sanitized?


class UserInput:
    def __init__(self, direction):
        self._direction = direction

    def __str__(self):
        #TODO should this still have a str method or should view.py take care of it
        return "UP" if self._direction == Direction.UP else "DOWN"

    def get_direction(self):
        return self._direction



class GameController(object):

    def __init__(self, num_floors, capacity):
        self._game = Bellhop(num_floors, capacity)

    def _on_input(self, s_input):
        self._user_input = s_input

    # todo MAX make obsolete
    def _collect_input(self):
        input_valid = False
        while not input_valid:
            text = input("Enter (u)p/(d)own:")
            if text.lower() in ('u', 'up', 'w'):
                self._on_input(UserInput(Direction.UP))
                input_valid = True
            elif text.lower() in ('d', 'down', 's'):
                self._on_input(UserInput(Direction.DOWN))
                input_valid = True
            elif text.lower() == 'q':
                exit(1) #filthy low level gutter dwelling scum code


    def run(self):
        while True:
            curr_state = self._game.get_state()
            if curr_state == State.WAIT_INPUT:
                self._collect_input()
                user_input = self._user_input #TODO this is gross
            else:
                user_input = None #TODO yuck
            self._game.step(user_input)
            time.sleep(0.1)


if __name__ == '__main__':
    game = GameController(4, 10)
    game.run()
