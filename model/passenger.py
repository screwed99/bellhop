class Passenger:
    id_num = 0
    def __init__(self, floor_entered: int, desired_floor: int):
        self._floor_entered: int = floor_entered
        self._desired_floor: int = desired_floor

# todo THIJS make passenger state enum
        self._in_elevator: bool = False
        self._dropped_off: bool = False
        self._id: int = Passenger.id_num
        Passenger.id_num += 1  # is this legit?

    def __str__(self):
        return "Pass[id: {} start:{} dest:{} in:{} drop: {}]"\
            .format(self._id,
                    self._floor_entered,
                    self._desired_floor,
                    self._in_elevator,
                    self._dropped_off)

    def get_desired_floor(self) -> int:
        return self._desired_floor

    def pick_up(self) -> None:
        assert(not self._in_elevator and not self._dropped_off)
        self._in_elevator = True
        print("Picked up passenger ", self._id) #TODO how does the viewer find out there was a pickup?

    def drop_off(self) -> None:
        assert(self._in_elevator)
        self._in_elevator = False
        self._dropped_off = True
        print("Dropped off passenger ", self._id)

    def is_waiting_for_pickup(self) -> bool:
        return not self._in_elevator and not self._dropped_off

    def is_in_elevator(self) -> bool:
        return self._in_elevator

    def is_dropped_off(self) -> bool:
        return self._dropped_off