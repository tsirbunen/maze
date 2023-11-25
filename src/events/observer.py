from abc import ABC, abstractmethod

from .event import AlgorithmEvent


class Observer(ABC):
    """Observer interface for an observer that observes maze algorithm-related events."""

    @abstractmethod
    def on_event(self, event: AlgorithmEvent):
        """Action to be performed when an event occurs."""
        pass
