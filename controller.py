import time

from model import Bellhop
from view import BellhopViewer, DebugView
from enums import State, Direction
from scratch import ConsoleView

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
        self._viewer = BellhopViewer(self._game)
        self._view = DebugView(self._viewer)

    # todo MAX make obsolete
    def _collect_input(self):
        input_valid = False
        while not input_valid:
            text = input("Enter (u)p/(d)own:")
            if text.lower() in ('u', 'up', 'w'):
                user_input = UserInput(Direction.UP)
                input_valid = True
            elif text.lower() in ('d', 'down', 's'):
                user_input = UserInput(Direction.DOWN)
                input_valid = True
            elif text.lower() == 'q':
                exit(1) #filthy low level gutter dwelling scum code
        return user_input

    def run(self):
        while True:
            #Model stuff
            curr_state = self._game.get_state()
            if curr_state == State.WAIT_INPUT:
                user_input = self._collect_input()
                self._game.step(user_input)
            else:
                self._game.step(None)

            #Viewer stuff
            self._viewer.update_model(self._game)
            self._view.run()

            #Control
            time.sleep(0.1)


class GameControllerConsoleView(object):
    """
    Maybe temp class, I just wanted this to iterate on ConsoleView class
    """

    def __init__(self, num_floors=4, capacity=10):
        self._game = Bellhop(num_floors, capacity)
        self._viewer = BellhopViewer(self._game)

        model_vars = dict(num_floors=num_floors, capacity=capacity)
        self._view = ConsoleView(self._viewer, model_vars)

    # todo MAX make obsolete
    def _collect_input(self):
        input_valid = False
        while not input_valid:
            text = input("Enter (u)p/(d)own:")
            if text.lower() in ('u', 'up', 'w'):
                user_input = UserInput(Direction.UP)
                input_valid = True
            elif text.lower() in ('d', 'down', 's'):
                user_input = UserInput(Direction.DOWN)
                input_valid = True
            elif text.lower() == 'q':
                exit(1) #filthy low level gutter dwelling scum code
        return user_input

    def run(self):
        while True:
            #Model stuff
            curr_state = self._game.get_state()
            if curr_state == State.WAIT_INPUT:
                user_input = self._collect_input()
                self._game.step(user_input)
            else:
                self._game.step(None)

            #Viewer stuff
            self._viewer.update_model(self._game)
            self._view.run()

            #Control
            time.sleep(0.1)



if __name__ == '__main__':
    game = GameControllerConsoleView(7, 10)
    game.run()
