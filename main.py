from controller import GameController
from model.model import Bellhop
from view import DebugView, ConsoleView, PyGameViewTextWriter
import pygame


def build_console_game_controller(num_floors=3, capacity=10):
    model = Bellhop(num_floors, capacity)
    size = 2000, 2000
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.font.init()
    font_size = 20
    pygame_font = pygame.font.SysFont('Courier New', font_size)
    writer = PyGameViewTextWriter(screen, pygame_font, font_size)
    model_vars = dict(num_floors=num_floors, capacity=capacity)
    view = ConsoleView(model, model_vars, writer)
    return GameController(model, view)

def build_debug_game_controller(num_floors=3, capacity=10):
    model = Bellhop(num_floors, capacity)
    size = 2000, 2000
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.font.init()
    font_size = 20
    pygame_font = pygame.font.SysFont('Courier New', font_size)
    writer = PyGameViewTextWriter(screen, pygame_font, font_size)
    view = DebugView(model, writer)
    return GameController(model, view)


if __name__ == '__main__':
    game = build_console_game_controller()
    clock = pygame.time.Clock()
    game.run(clock)
