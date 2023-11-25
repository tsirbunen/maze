import threading
import time
from src.events.event import EventType
from src.events.event_queue import EventQueue
from src.graphical_ui.stamp_activity import StampActivity


def threaded(fn):
    """Decorator that makes a function run in a new thread"""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class EventsProcessor:
    """Uses events produced by maze algorithms to show their progress on the screen."""

    _sleep_time = 2
    _should_stop_processing = False
    _temporary_nodes = []
    _with_live_viewing = True

    def __init__(
        self,
        queue: EventQueue,
        handle_stamp_action_fn,
        remove_wall_fn,
        perform_next_step,
    ):
        self._queue = queue
        self._handle_stamp_action = handle_stamp_action_fn
        self._remove_wall = remove_wall_fn
        self.available_actions = {
            EventType.MAZE_GENERATION_COMPLETED: self._on_maze_completed,
            EventType.PHASE_COMPLETED: self._hide_all_stamps,
            EventType.PERMANENT_NODE: self._show_stamps,
            EventType.REMOVE_WALL: self._remove_wall,
            EventType.TEMPORARY_ROOT: self._set_temporary_root_node,
            EventType.TEMPORARY_NEIGHBOR: self._add_temporary_neighbor_node,
            EventType.SOLVING_COMPLETED: self._on_solving_completed,
            EventType.PATH_NODE: self._show_path_node,
            EventType.BLINK_NODE: self._blink_node,
        }
        self.perform_next_step = perform_next_step

    def lower_speed(self):
        """Slows down the speed with which the processor moves on to show the next event."""
        self._sleep_time *= 2

    def higher_speed(self):
        """Speeds up the speed with which the processor moves on to show the next event."""
        self._sleep_time /= 2

    def stop_processing(self, _=None):
        """Stops showing progress live on the screen."""
        self._should_stop_processing = True
        self._handle_stamp_action(StampActivity.HIDE_ALL, None)

    def hide_live_viewing(self):
        """Control whether the processor shows progress live on the screen."""
        self._with_live_viewing = False

    @threaded
    def process(self):
        """Translates maze algorithm events into animations on the screen."""
        self._reset_stamp_colors()
        if self._should_stop_processing:
            self._should_stop_processing = False
        while not self._should_stop_processing:
            time.sleep(self._sleep_time)
            if not self._queue.is_empty():
                event = self._queue.next_event()
                action = self.available_actions[event.algorithm_event_type]
                action(event.nodes)
        self.stop_processing()

    def _reset_stamp_colors(self):
        self._handle_stamp_action(StampActivity.RESET_ALL, None)

    def _hide_all_stamps(self, _):
        self._handle_stamp_action(StampActivity.HIDE_ALL, None)

    def _show_stamps(self, nodes):
        for node in nodes:
            self._handle_stamp_action(StampActivity.SHOW_STAMP, node)

    def _hide_stamps(self, nodes):
        for node in nodes:
            self._handle_stamp_action(StampActivity.HIDE_STAMP, node)

    def _set_temporary_root_node(self, nodes):
        self._hide_earlier__temporary_nodes()
        self._temporary_nodes = [nodes[0]]
        self._handle_stamp_action(StampActivity.SHOW_STAMP, nodes[0])

    def _hide_earlier__temporary_nodes(self):
        while len(self._temporary_nodes) > 0:
            node = self._temporary_nodes.pop()
            self._handle_stamp_action(StampActivity.HIDE_STAMP, node)

    def _add_temporary_neighbor_node(self, nodes):
        self._temporary_nodes.append(nodes[0])
        self._handle_stamp_action(StampActivity.SHOW_STAMP, nodes[0])

    def _show_path_node(self, nodes):
        self._handle_stamp_action(StampActivity.SHOW_PATH_STAMP, nodes[0])

    def _blink_node(self, nodes):
        self._handle_stamp_action(StampActivity.BLINK_STAMP, nodes[0])
        self._handle_stamp_action(StampActivity.SHOW_STAMP, nodes[0])

    def _on_solving_completed(self, _):
        time.sleep(2)
        self.stop_processing()
        self.perform_next_step()

    def _on_maze_completed(self, maze_connections):
        if self._with_live_viewing:
            self._should_stop_processing = True
        else:
            self._remove_maze_walls(maze_connections)
            self._with_live_viewing = True
        self.perform_next_step(maze_connections)

    def _remove_maze_walls(self, maze_connections):
        for index, connections_of_a_node in enumerate(maze_connections):
            for neighbor in connections_of_a_node:
                self._remove_wall([index, neighbor], False)
