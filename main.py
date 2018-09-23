import argparse

import pygame

from controller.controller import GameController
from controller.debug_controller import DebugGameController
from model.model import Bellhop
from view.view import ConsoleView, PyGameViewTextWriter
from view.debug_view import DebugView


def build_game_controller(num_floors=3, capacity=10) -> GameController:
    model = Bellhop(num_floors, capacity)
    size = 1920, 1080
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.font.init()
    font_size = 20
    pygame_font = pygame.font.SysFont('Courier New', font_size)
    writer = PyGameViewTextWriter(screen, pygame_font, font_size)
    model_vars = dict(num_floors=num_floors, capacity=capacity)
    view = ConsoleView(model, model_vars, writer)
    return GameController(model, view)

def build_debug_game_controller(num_floors=3, capacity=10) -> DebugGameController:
    model = Bellhop(num_floors, capacity)
    view = DebugView(model)
    return DebugGameController(model, view)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Best bellhop discrete game.')
    parser.add_argument('--mode', type=str, default='prod', help='possible flags [debug]')

    args = parser.parse_args()
    if args.mode == 'debug':
        game = build_debug_game_controller()
        game.run()
    else:
        game = build_game_controller()
        clock = pygame.time.Clock()
        game.run(clock)
