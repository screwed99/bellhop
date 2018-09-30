import time
from controller.i_controller import IController
from model.model import Bellhop
from view.i_view import IView
from enums import State, Direction


class DebugGameController(IController):

    def __init__(self, game: Bellhop, view: IView) -> None:
        self._game: Bellhop = game
        self._view: IView = view

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
            self._view.paint()

            #Control
            time.sleep(0.1)

