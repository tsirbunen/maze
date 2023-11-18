import threading
import time
from src.events.event import EventType
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


class EventsProcessor:
    """Uses events produced by maze algorithms to show their progress on the screen."""

    def __init__(
        self,
        queue: EventQueue,
        stamps: StatusStamps,
        walls: MazeWalls,
        move_on_to_next_step,
    ):
        self._sleep_time = 2
        self._queue = queue
        self.stamps = stamps
        self.walls = walls
        self.temporary_nodes = []
        self.should_stop_processing = False
        self.available_actions = {
            EventType.MAZE_GENERATION_COMPLETED: self._maze_completed,
            EventType.PHASE_COMPLETED: self._hide_all_stamps,
            EventType.PERMANENT_NODE: self._show_stamps,
            EventType.REMOVE_WALL: self.remove_wall,
            EventType.TEMPORARY_ROOT: self._set_temporary_root_node,
            EventType.TEMPORARY_NEIGHBOR: self._add_temporary_neighbor_node,
            EventType.SOLVING_COMPLETED: self._solving_completed,
        }
        self.move_on_to_next_step = move_on_to_next_step

    def lower_speed(self):
        """Slows down the speed with which the processor moves on to show the next event."""
        self._sleep_time *= 2

    def higher_speed(self):
        """Speeds up the speed with which the processor moves on to show the next event."""
        self._sleep_time /= 2

    def stop_processing(self):
        """Stops showing progress live on the screen."""
        self.should_stop_processing = True
        self.stamps.hide_all()
        self.move_on_to_next_step()

    def _hide_all_stamps(self, _):
        self.stamps.hide_all()

    def _show_stamps(self, nodes):
        for node in nodes:
            self.stamps.show_stamp(node)

    def _hide_stamps(self, nodes):
        for node in nodes:
            self.stamps.hide_stamp(node)

    def remove_wall(self, nodes):
        self.walls.remove_wall_between_nodes_with_a_blink(nodes)

    def _set_temporary_root_node(self, nodes):
        self._hide_earlier_temporary_nodes()
        self.temporary_nodes = [nodes[0]]
        self.stamps.show_stamp(nodes[0])

    def _hide_earlier_temporary_nodes(self):
        while len(self.temporary_nodes) > 0:
            node = self.temporary_nodes.pop()
            self.stamps.hide_stamp(node)

    def _add_temporary_neighbor_node(self, nodes):
        self.temporary_nodes.append(nodes[0])
        self.stamps.show_stamp(nodes[0])

    def _maze_completed(self, _):
        self._set_should_stop(None)

    def _solving_completed(self, _):
        self._hide_all_stamps(None)

    def _set_should_stop(self, _):
        self.should_stop_processing = True

    @threaded
    def process(self):
        """Processes maze algorithm events in the queue."""
        while not self.should_stop_processing:
            print("\033[95mCheck for new events...")
            time.sleep(self._sleep_time)
            if not self._queue.is_empty():
                event = self._queue.next_event()
                print(f"\033[95mProcess: {event.algorithm_event_type} - {event.nodes}")
                action = self.available_actions[event.algorithm_event_type]
                action(event.nodes)
        self.stop_processing()
