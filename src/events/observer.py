from abc import ABC, abstractmethod

from .event import AlgorithmEvent


class Observer(ABC):
    @abstractmethod
    def on_event(self, event: AlgorithmEvent):
        pass
