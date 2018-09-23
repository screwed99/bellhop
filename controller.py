from model.model import Bellhop
from view import ViewInterface
from enums import State, Direction
import pygame
import sys


class GameController(object):

    def __init__(self, game: Bellhop, view: ViewInterface):
        self._game = game
        self._view = view

    # TODO extract input to a pygame version so we can get a debug console version still
    def _collect_input(self):
        input_valid = False
        user_input = None
        while not input_valid:
            event = pygame.event.poll()
            while event.type != pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                event = pygame.event.poll()
            if event.key == pygame.K_u:
                input_valid = True
                user_input = Direction.UP
            elif event.key == pygame.K_d:
                input_valid = True
                user_input = Direction.DOWN
        return user_input

    def run(self, clock):
        while True:
            curr_state = self._game.get_state()
            if curr_state == State.WAIT_INPUT:
                user_input = self._collect_input()
                self._game.step(user_input)
            else:
                self._game.step(None)

            self._view.paint()
            pygame.display.flip()

            clock.tick(30)
