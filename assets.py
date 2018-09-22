import os

#from controller import GameControllerConsoleView
#game = GameControllerConsoleView()
#game.run()

class Assets(object):
    PERSON = """
  \|||/
6 (o o) 
|  (_) 
--|   |--
  |___| |
  | | | 9
 ( ] [ )
""".strip("\n")

    FLOOR = """
+====================================================+
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
||                                                  ||
+====================================================+
""".strip("\n")

    FLOOR_FLOOR_THICKNESS = 1

    ELEVATOR = """
______________________________________________________________
|-__________________________________________________________-|
||                                                          ||
||                                                          ||
||                                                          ||
||                                                          ||
||                                                          ||
||                                                          ||
||                                                          ||
|-__________________________________________________________-|
|____________________________________________________________| 
""".strip("\n")

    ELEVATOR_FLOOR_THICKNESS = 2

#model_vars = dict(num_floors=4, capacity=14)
#cv = ConsoleView(None, model_vars)
#cv.run()