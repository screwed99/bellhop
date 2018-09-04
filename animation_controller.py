PASSENGER_X = 10
PASSENGER_Y = 10
PASSENGER_X_LEN = 30
PASSENGER_Y_LEN = 30

class AnimationHandler:

    def __init__(self):
        self._curr_animation = None

    def is_animation(self):
        return self._curr_animation is not None

    def iterate_animation(self):
        if self._curr_animation is None:
            raise Exception("Cannot iterate non-existent animation!")
        if self._curr_animation.step():
            self._curr_animation = None

    def set_new_animation(self, animation):
        if self._curr_animation is not None:
            raise Exception("Cannot set animation while one is in progress!")
        self._curr_animation = animation

class PassengersLeaveAnimation:

    def __init__(self, view_passengers, view_passenger_manager):
        self._view_passengers = view_passengers
        self._view_passenger_manager = view_passenger_manager

    def step(self):
        new_view_passengers = []
        for view_passenger in self._view_passengers:
            steps_left = view_passenger.step_leave()
            if steps_left:
                new_view_passengers.append(view_passenger)
            else:
                self._view_passenger_manager.remove_from_view(view_passenger)
        self._view_passengers = new_view_passengers
        return not self._view_passengers

class ViewPassengerManager:

    def __init__(self, passenger_capacity, animation_handler, view_dimensions, leave_speed, display_surface):
        if passenger_capacity <= 0:
            raise Exception("Need positive passenger capacity!, not {0}".format(passenger_capacity))
        self._view_passengers = [None] * passenger_capacity
        self._animation_handler = animation_handler
        self._view_dimensions = view_dimensions
        self._leave_speed = leave_speed
        self._display_surface = display_surface

    def passengers_enter(self, passengers):
        for passenger in passengers:
            self._passenger_enters(passenger)

    def _passenger_enters(self, passenger):
        next_empty_spot_index = 0
        while next_empty_spot_index < len(self._view_passengers):
            if self._view_passengers[next_empty_spot_index] is None:
                passenger_x = PASSENGER_X + (next_empty_spot_index * 30)
                passenger_y = PASSENGER_Y + (next_empty_spot_index * 30)
                passenger_view_dimensions = ViewDimensions(passenger_x, passenger_y, PASSENGER_X_LEN, PASSENGER_Y_LEN)
                view_passenger = ViewPassenger(passenger, passenger_view_dimensions, self._view_dimensions, self._leave_speed)
                self._view_passengers[next_empty_spot_index] = view_passenger
                return
            next_empty_spot_index += 1
        raise Exception("Added too many passengers to elevator!")

    def get_view_passengers(self):
        return (x for x in self._view_passengers if x is not None)

    def remove_from_view(self, view_passenger):
        for i in range(len(self._view_passengers)):
            if view_passenger == self._view_passengers[i]:
                self._view_passengers[i] = None
                return
        raise Exception("Could not remove view passenger!")

    def passengers_leave(self, desired_floor):
        leaving_view_passengers = []
        for i in range(len(self._view_passengers)):
            view_passenger = self._view_passengers[i]
            if view_passenger is not None and \
                    view_passenger.get_desired_floor() == desired_floor:
                leaving_view_passengers.append(view_passenger)
        passengers_leave_animation = PassengersLeaveAnimation(leaving_view_passengers, self)
        self._animation_handler.set_new_animation(passengers_leave_animation)

class ViewPassenger:

    def __init__(self, passenger, passenger_view_dimensions, view_dimensions, leave_speed):
        self._passenger = passenger
        self._passenger_view_dimensions = passenger_view_dimensions
        self._view_dimensions = view_dimensions
        self._leave_speed = leave_speed

    def get_desired_floor(self):
        return self._passenger.get_desired_floor()

    def get_passenger_view_dimensions(self):
        return self._passenger_view_dimensions

    def step_leave(self):
        self._passenger_view_dimensions.move(self._leave_speed)
        return self._passenger_view_dimensions.is_overlap(self._view_dimensions)

class ViewDimensions:

    def __init__(self, x, y, x_len, y_len):
        self._x = x
        self._y = y
        self._x_len = x_len
        self._y_len = y_len

    def get_left_corner(self):
        return (self._x, self._y)

    def move(self, speed):
        speed_x, speed_y = speed[0], speed[1]
        self._x += speed_x
        self._y += speed_y

    def is_overlap(self, other_view_dimensions):
        # TODO FIX!
        return self._x < other_view_dimensions._x + other_view_dimensions._x_len


