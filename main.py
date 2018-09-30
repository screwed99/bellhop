import argparse
import pygame

from controller.controller import BellhopController
from controller.debug_controller import DebugGameController
from model.model import BellhopModel
from view.console_view import ConsoleView, PyGameViewTextWriter
from view.debug_view import DebugView
from view.view import BellhopView, PyGameImageWriter
from typing import Any


def build_game_controller(width, height, num_floors=3, capacity=10) -> BellhopController:
    model = BellhopModel(num_floors, capacity)
    size = width, height
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.font.init()
    font_size = 20
    pygame_font = pygame.font.SysFont('Courier New', font_size)
    writer = PyGameViewTextWriter(screen, pygame_font, font_size)
    model_vars = dict(num_floors=num_floors, capacity=capacity)
    view = ConsoleView(model, model_vars, writer)
    return BellhopController(model, view)

def build_visuals_controller(width, height, num_floors=3, capacity=5) -> BellhopController:
    model = BellhopModel(num_floors, capacity)
    size = width, height
    pygame.init()
    screen = pygame.display.set_mode(size)
    writer = PyGameImageWriter(screen)
    model_vars = dict(num_floors=num_floors, capacity=capacity)
    view = BellhopView(model, model_vars, writer)
    return BellhopController(model, view)

def build_debug_game_controller(num_floors=3, capacity=10) -> DebugGameController:
    model = BellhopModel(num_floors, capacity)
    view = DebugView(model)
    return DebugGameController(model, view)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Best bellhop discrete game.')
    parser.add_argument('-m', '--mode', type=str, default='prod', choices=['prod', 'debug', 'visual'], help='run mode')
    parser.add_argument('-x', '--width', type=int, default='1920', help='window width in px')
    parser.add_argument('-y', '--height', type=int, default='1080', help='window height in px')

    game: Any = None
    args = parser.parse_args()
    if args.mode == 'debug':
        game = build_debug_game_controller()
        game.run()
    elif args.mode == 'visual':
        game = build_visuals_controller(width=args.width, height=args.height)
        clock = pygame.time.Clock()
        game.run(clock)
    else:
        game = build_game_controller(width=args.width, height=args.height)
        clock = pygame.time.Clock()
        game.run(clock)
