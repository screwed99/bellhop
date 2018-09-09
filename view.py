from model import BellhopViewInterface

"""
# controls
# todo THIJS link this with new passenger gen
self._indicators_lit = {key: False for key in range(0, self._num_floors)}

# door
self._elevator_moving = False
"""

class BellhopViewer(BellhopViewInterface):
    """
    A possibly ridiculous way to pass the game instance to Viewers in a way that implements the interface.
    Viewer classes should only ever have to call an instance of this class
    It is the controller's job to push updates to the model with update_model
    """

    def __init__(self, model):
        self.model = model  # TODO make sure this is a Bellhop instance

    def update_model(self, new_model):
        self.model = new_model

    def get_state(self):
        return self.model.get_state()

    def get_elevator_contents(self):
        return self.model.get_elevator_contents()

    def get_people_waiting(self):
        return self.model.get_people_waiting()

    def get_current_floor(self):
        return self.model.get_current_floor()


class DebugView(object):

    def __init__(self, bellhop_viewer):
        self._bellhop_viewer = bellhop_viewer

    def print_game(self):
        print(self)

    def run(self):
        self.print_game()

    def __str__(self):
        ret = "{} ON {} | ".format(self._bellhop_viewer.get_state(), self._bellhop_viewer.get_current_floor())
        ret += "\n|----- Elevator -----|\n"
        people_in = self._bellhop_viewer.get_elevator_contents()
        for x in people_in:
            ret += "| {} |\n".format(x)
        ret += "|____________________|\n"
        people_waiting = self._bellhop_viewer.get_people_waiting()
        for x in people_waiting:
            ret += "{}\n".format(x)
            for y in people_waiting[x]:
                ret += "{} ".format(y)
            ret += "\n"
        return ret
