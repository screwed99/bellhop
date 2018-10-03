import argparse
import pygame
from typing import Any

from controller.controller import BellhopController
from controller.debug_controller import DebugGameController
from levels.level import Level
from levels.level_parser import LevelParser
from model.model import BellhopModel
from view.console_view import ConsoleView, PyGameViewTextWriter
from view.debug_view import DebugView
from view.view import BellhopView, PyGameImageWriter


def get_parsed_level(level_path: str):
    parser = LevelParser(level_path)
    level = parser.parse_from_file()
    return level


def build_game_controller(width: int, height: int, level_path: str) -> BellhopController:
    level = get_parsed_level(level_path)
    model = BellhopModel(level)
    size = width, height
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.font.init()
    font_size = 18
    pygame_font = pygame.font.SysFont('Courier New', font_size)
    writer = PyGameViewTextWriter(screen, pygame_font, font_size)
    model_vars = dict(num_floors=level.get_num_floors(), capacity=level.get_capacity()) #TODO interf include these vars
    view = ConsoleView(model, model_vars, writer)
    return BellhopController(model, view)


def build_visuals_controller(width: int, height: int, level_path: str) -> BellhopController:
    level = get_parsed_level(level_path)
    model = BellhopModel(level)
    size = width, height
    pygame.init()
    screen = pygame.display.set_mode(size)
    writer = PyGameImageWriter(screen)
    model_vars = dict(num_floors=level.get_num_floors(), capacity=level.get_capacity()) #TODO interf include these vars
    view = BellhopView(model, model_vars, writer)
    return BellhopController(model, view)


def build_debug_game_controller(level_path: str) -> DebugGameController:
    level = get_parsed_level(level_path)
    model = BellhopModel(level)
    view = DebugView(model)
    return DebugGameController(model, view)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Best bellhop discrete game.')
    parser.add_argument('-m', '--mode', type=str, default='prod', choices=['prod', 'debug', 'visual'], help='run mode')
    parser.add_argument('-x', '--width', type=int, default='1920', help='window width in px')
    parser.add_argument('-y', '--height', type=int, default='1080', help='window height in px')
    parser.add_argument('-l', '--level', type=str, default='example', help='name of level w/o path or extension')

    game: Any = None
    args = parser.parse_args()
    level_path = "levels/" + args.level + ".txt"

    if args.mode == 'debug':
        game = build_debug_game_controller(level_path=level_path)
        game.run()
    elif args.mode == 'visual':
        game = build_visuals_controller(width=args.width, height=args.height, level_path=level_path)
        clock = pygame.time.Clock()
        game.run(clock)
    else:
        game = build_game_controller(width=args.width, height=args.height, level_path=level_path)
        clock = pygame.time.Clock()
        game.run(clock)
