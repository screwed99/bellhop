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
        user_input = None
        events = pygame.event.get()
        if len(events) == 0:
            return user_input
        else:
            event = events[-1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                user_input = Direction.UP
            elif event.key == pygame.K_d:
                user_input = Direction.DOWN
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
