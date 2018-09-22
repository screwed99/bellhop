from controller import GameController
from model.model import Bellhop
from view import DebugView, ConsoleView

def build_console_game_controller(num_floors=4, capacity=10):
    model = Bellhop(num_floors, capacity)
    model_vars = dict(num_floors=num_floors, capacity=capacity)
    view = ConsoleView(model, model_vars)
    return GameController(model, view)

def build_debug_game_controller(num_floors=3, capacity=10):
    model = Bellhop(num_floors, capacity)
    view = DebugView(model)
    return GameController(model, view)


if __name__ == '__main__':
    game = build_console_game_controller()
    game.run()