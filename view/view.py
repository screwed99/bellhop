import pygame

from view.interfaces import IView
from model.interfaces import IBellhopViewer
from typing import Dict, Tuple


class PyGameImageWriter:

    def __init__(self, screen):
        self._screen = screen

    def write(self, image, position: Tuple[int, int]) -> None:
        self._screen.blit(image, position)


class BellhopView(IView):
    def __init__(self, bellhop_model: IBellhopViewer, model_vars: Dict[str, int], writer: PyGameImageWriter) -> None:
        self._bellhop_model = bellhop_model
        self._num_floors = model_vars['num_floors']
        self._capacity = model_vars['capacity']
        self._writer = writer

        # load assets
        self._door = pygame.image.load("assets/door.png")
        self._console = pygame.image.load("assets/console.png")
        self._indicator_sheet = pygame.image.load("assets/indicator.png")

    def paint(self):
        self.print_game()

    def print_game(self):
        self._writer.write(self._door, (100, 200))
        self._writer.write(self._console, (400, 100))
        self._writer.write(self._indicator_sheet, (410, 250))
