from .event import AlgorithmEvent
from .event_queue import EventQueue

from .observer import Observer

QUEUE_MAX_SIZE = 10


class QueueObserver(Observer):
    """Tracks maze algorithm events and puts them in a queue for a processor to handle"""

    def __init__(self, queue: EventQueue) -> None:
        super().__init__()
        self._queue = queue

    def on_event(self, event):
        self._queue.enqueue(event)

    def is_empty(self) -> bool:
        """Tells whether there are any events in the queue at the moment"""
        return self._queue.empty()

    def next_event(self) -> AlgorithmEvent | None:
        """Gives the next event in queue if there are any"""
        if not self._queue.empty():
            return self._queue.get()
        return None
