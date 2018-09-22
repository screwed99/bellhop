from model.passenger import Passenger


class GaggleOfPassengers:
    def __init__(self):
        self._passengers = []

    def add_passenger(self, passenger: Passenger) -> None:
        self._passengers.append(passenger)

    def get_passengers_in_elevator(self) -> [Passenger]:
        return [passenger for passenger in self._passengers if passenger._in_elevator]

    def get_passengers_waiting(self) -> [Passenger]:
        return [passenger for passenger in self._passengers if passenger.is_waiting_for_pickup()]

    def get_passengers_waiting_by_floor(self) -> {int, Passenger}:
        waiting_by_floor = {}
        for passenger in self.get_passengers_waiting():
            floor = passenger._floor_entered
            if floor not in waiting_by_floor:
                waiting_by_floor[floor] = []
            waiting_by_floor[floor].append(passenger)
        return waiting_by_floor

    def pick_up(self, floor: int) -> None:
        for passenger in self.get_passengers_waiting_by_floor().get(floor, []):
            passenger.pick_up()

    def drop_off(self, floor: int) -> None:
        for passenger in self.get_passengers_in_elevator():
            if passenger._desired_floor == floor:
                passenger.drop_off()