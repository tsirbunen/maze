from abc import ABC, abstractmethod

from .event import Event

class Observer(ABC):
    @abstractmethod
    def on_event(self, event: Event):
        pass