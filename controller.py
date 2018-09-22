import time

from model.model import Bellhop
from view import BellhopViewer, DebugView
from enums import State, Direction
from scratch import ConsoleView



class GameController(object):

    def __init__(self, num_floors, capacity):
        self._game = Bellhop(num_floors, capacity)
        self._viewer = BellhopViewer(self._game)
        self._view = DebugView(self._viewer)

    def _collect_input(self):
        input_valid = False
        user_input = None
        while not input_valid:
            text = input("Enter (u)p/(d)own:")
            if text.lower() in ('u', 'up', 'w'):
                user_input = Direction.UP
                input_valid = True
            elif text.lower() in ('d', 'down', 's'):
                user_input = Direction.DOWN
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
            self._viewer.update_model(self._game) # is it necessary to replace the model or do they share a reference?
            self._view.run()

            #Control
            time.sleep(0.1)


class ConsoleViewGameController(GameController):

    def __init__(self, num_floors: int=4, capacity: int=10):
        GameController.__init__(self, num_floors, capacity)
        model_vars = dict(num_floors=num_floors, capacity=capacity)
        self._view = ConsoleView(self._viewer, model_vars)



if __name__ == '__main__':
    game = ConsoleViewGameController(3, 10)
    game.run()
