import time
from typing import Optional

from enums import State, Direction
from controller.interfaces import IController
from model.interfaces import IBellhopController
from view.interfaces import IView


class DebugGameController(IController):

    def __init__(self, game: IBellhopController, view: IView) -> None:
        self._game: IBellhopController = game
        self._view: IView = view

    def _collect_input(self):
        input_valid: bool = False
        user_input: Optional[Direction] = None
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

