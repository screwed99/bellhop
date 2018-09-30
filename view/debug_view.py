import os

from enums import State
from model.interfaces import IBellhopViewer
from view.interfaces import IView


class DebugView(IView):

    def __init__(self, bellhop_model: IBellhopViewer, clear: bool=False) -> None:
        self._bellhop_model: IBellhopViewer = bellhop_model
        self._clear: bool = clear

    def paint(self) -> None:
        if self._clear:
            os.system('clear')
        if self._bellhop_model.get_state() == State.WAIT_INPUT:
            print(self)

    def __str__(self):
        ret = "{} ON {} | ".format(self._bellhop_model.get_state(), self._bellhop_model.get_current_floor())
        ret += "\n|----- Elevator -----|\n"
        people_in = self._bellhop_model.get_elevator_contents()
        for x in people_in:
            ret += "| {} |\n".format(x)
        ret += "|____________________|\n"
        people_waiting = self._bellhop_model.get_people_waiting()
        for x in people_waiting:
            ret += "{}\n".format(x)
            for y in people_waiting[x]:
                ret += "{} ".format(y)
            ret += "\n"
        return ret