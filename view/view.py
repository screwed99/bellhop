import pygame

from view.interfaces import IView
from model.interfaces import IBellhopViewer
from typing import Dict, Tuple

class PyGameImage:

    def __init__(self, image: pygame.Surface) -> None:
        self._image: pygame.Surface = image
        self._rect: pygame.Rect = self._image.get_rect()

    def move(self, x_off: int, y_off: int) -> None:
        self._rect.move_ip(x_off, y_off)

    def get_width(self) -> int:
        ret = self._image.get_width()
        if ret == None:
            return 0
        return int(ret)

    def get_height(self) -> int:
        ret = self._image.get_height()
        if ret == None:
            return 0
        return int(ret)

    def get_position(self) -> Tuple[int, int]:
        ret = self._rect.topleft
        if ret == None:
            return (0, 0)
        return (ret[0], ret[1])

    def get_x(self) -> int:
        return self.get_position()[0]

    def get_y(self) -> int:
        return self.get_position()[1]

    def get_surface(self) -> pygame.Surface:
        return self._image

    def get_surface_copy(self) -> pygame.Surface:
        return self._image.copy()


class PyGameImageWriter:

    def __init__(self, screen: pygame.Surface) -> None:
        self._screen: pygame.SurfaceType = screen

    def write(self, image: PyGameImage) -> None:
        self._screen.blit(image.get_surface(), image.get_position())


class BellhopView(IView):
    def __init__(self, bellhop_model: IBellhopViewer, model_vars: Dict[str, int], writer: PyGameImageWriter) -> None:
        self._bellhop_model: IBellhopViewer = bellhop_model
        self._num_floors: int = model_vars['num_floors']
        self._capacity: int = model_vars['capacity']
        self._writer: PyGameImageWriter = writer

        # load assets
        self._left_door: PyGameImage = PyGameImage(pygame.image.load("assets/door.png").convert_alpha())

        self._right_door: PyGameImage = PyGameImage(self._left_door.get_surface_copy())
        self._right_door.move(self._left_door.get_x() + self._left_door.get_width(), 0)

        self._elevator: PyGameImage = PyGameImage(pygame.image.load("assets/elevator.png").convert_alpha())
        self._elevator.move(self._right_door.get_x() + self._right_door.get_width(), 0)

        self._console: PyGameImage = PyGameImage(pygame.image.load("assets/console.png").convert_alpha())
        self._console.move(self._elevator.get_x() + self._elevator.get_width(), 0)
        # # todo figure out how the pygame sprite classes work
        # self._indicator_sheet: pygame.Surface = pygame.image.load("assets/indicator.png").convert_alpha()

    def paint(self) -> None:
        self.print_game()

    def print_game(self) -> None:
        self._writer.write(self._left_door)
        self._writer.write(self._right_door)
        self._writer.write(self._elevator)
        self._writer.write(self._console)
