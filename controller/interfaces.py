import abc


class IController(abc.ABC):

    @abc.abstractmethod
    def run(self, *args, **kwargs) -> None:
        pass