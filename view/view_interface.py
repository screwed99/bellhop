import abc


class ViewInterface(abc.ABC):

    @abc.abstractmethod
    def paint(self) -> None:
        pass