import abc


class IView(abc.ABC):

    @abc.abstractmethod
    def paint(self) -> None:
        pass