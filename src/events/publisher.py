from abc import ABC, abstractmethod

from .observer import Observer
from .event import AlgorithmEvent


class Publisher(ABC):
    """Publisher interface for a publisher that publishes maze algorithm-related events."""

    @abstractmethod
    def attach_observer(self, observer: Observer):
        """Attaches an observer to the publisher."""

    @abstractmethod
    def detach_observer(self, observer: Observer):
        """Detaches an observer from the publisher."""

    @abstractmethod
    def dispatch_event(self, event: AlgorithmEvent):
        """Dispatches an event to all observers."""
