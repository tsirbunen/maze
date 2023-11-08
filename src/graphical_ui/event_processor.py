import threading
import time
from src.events.event import Event, EventType
from src.events.event_queue import EventQueue

from src.graphical_ui.maze_walls import MazeWalls
from src.graphical_ui.status_stamps import StatusStamps


def threaded(fn):
    """Decorator that makes a function run in a new thread"""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class EventProcessor:
    """Uses events produced by maze algorithms to show their progress on the screen."""

    def __init__(self, queue: EventQueue, stamps: StatusStamps, walls: MazeWalls):
        self._sleep_time = 2
        self._queue = queue
        self.stamps = stamps
        self.walls = walls
        self.merge_pair = []
        self._merge_focus_node = None
        self._merge_neighbor_node = None

    def lower_speed(self):
        """Slows down the speed with which the processor moves on to show the next event."""
        self._sleep_time *= 2

    def higher_speed(self):
        """Speeds up the speed with which the processor moves on to show the next event."""
        self._sleep_time /= 2

    @threaded
    def process(self):
        """Processes maze algorithm events in the queue."""
        print("Starting handle_events")
        while True:
            print("\033[95m--------  check for possible new items")
            time.sleep(self._sleep_time)
            if not self._queue.is_empty():
                event = self._queue.next_event()
                print(
                    f"\033[95mEvent HANDLER: {event.event_type} FROM: {event.from_node} TO: {event.to_node}"
                )
                self._process_event(event)

    def _process_event(self, event: Event):
        match event.event_type:
            case EventType.PHASE_COMPLETED:
                self.stamps.hide_all_stamps()
            case EventType.TWIST:
                self._process_twist_event(event)
            case EventType.MERGE_FOCUS:
                self._process_merge_focus_event(event)
            case EventType.MERGE_CONNECT:
                self._process_merge_connect_event(event)
            case _:
                raise ValueError(f"Event type {event.event_type} not implemented")

    def _process_twist_event(self, event: Event):
        if event.to_node is None:
            self.stamps.show_stamp(event.from_node)
        else:
            self.stamps.show_stamp(event.to_node)
            self.walls.remove_wall_between_nodes_with_a_blink(
                [event.from_node, event.to_node]
            )

    def _process_merge_focus_event(self, event: Event):
        if self._merge_neighbor_node is not None:
            self.stamps.hide_stamp(self._merge_neighbor_node)
        if self._merge_focus_node is not None:
            self.stamps.hide_stamp(self._merge_focus_node)
        self._merge_focus_node = event.from_node
        self.stamps.show_stamp(event.from_node)

    def _process_merge_connect_event(self, event: Event):
        self._merge_neighbor_node = event.to_node
        self.stamps.show_stamp(event.to_node)
        self.walls.remove_wall_between_nodes_with_a_blink(
            [event.from_node, event.to_node]
        )
