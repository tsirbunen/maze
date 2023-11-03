from abc import ABC, abstractmethod

from .observer import Observer
from .event import Event

class Publisher(ABC):
    @abstractmethod
    def attach_observer(self, observer: Observer):
        pass

    @abstractmethod
    def detach_observer(self, observer: Observer):
        pass

    @abstractmethod
    def dispatch_event(self, event: Event):
        pass