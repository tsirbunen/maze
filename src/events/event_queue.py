from queue import Queue
from src.events.event import AlgorithmEvent


class EventQueue:
    """A wrapped singleton queue (FIFO) that holds events related to maze algorithms' progress."""

    _instance = None
    _queue = Queue()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventQueue, cls).__new__(cls)
        return cls._instance

    def get_queue(self) -> Queue:
        """Returns the singleton instance of the one and only queue with events."""
        return self._instance

    def enqueue(self, event: AlgorithmEvent) -> None:
        """Add new event to the que"""
        self._queue.put(event, block=True)

    def is_empty(self) -> bool:
        """Tells whether there are any events in the event queue (at the moment of querying)."""
        return self._queue.empty()

    def next_event(self) -> AlgorithmEvent | None:
        """Gives the next event in the event queue if there are any (at the moment or querying)."""
        if not self._queue.empty():
            return self._queue.get()
        return None
