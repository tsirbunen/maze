import time
from maze_activity import MazeActivity
from src.events.event_queue import EventQueue
from src.graphical_ui.event_processor import EventProcessor

# from src.maze_generation.maze_generator import MazeGenerator
# from src.maze_parameters.maze_parameters import MazeParameters
# from src.maze_parameters.maze_type import MazeType

from .status_stamps import StatusStamps
from .maze_border import MazeBorder
from .maze_walls import MazeWalls
from .point import Point
from .constants import ELEMENT_SIZE
from .screen_provider import ScreenProvider


class GraphicalUI:
    """GraphicalUI is responsible for ORCHESTRATING all maze related things."""

    def __init__(
        self,
        maze_size: int,
        event_queue: EventQueue,
        perform_activity
        # self,
        # maze_size: int,
        # event_queue: EventHandler,
        # perform_activity,
    ) -> None:
        self._perform_activity = perform_activity
        self.screen_provider = ScreenProvider()
        self.update_screen = self.screen_provider.update
        self.origo = self._get_maze_origo(maze_size)
        self.walls = MazeWalls(self.origo, maze_size, self.update_screen)
        self.status_stamps = StatusStamps(self.origo, maze_size, self.update_screen)
        self._setup_border_walls_and_status_stamps(maze_size)

        # parameters = MazeParameters(4, MazeType.SINGLE)
        self.event_processor = EventProcessor(
            event_queue,
            self.status_stamps,
            self.walls,
        )
        # event_queue.process()
        self._setup_event_detection()
        # maze_generator.generate()
        # maze_connection = maze_generator.get_finished_maze()
        self.screen_provider.set_exit_on_click()

    def print_test(self):
        print("TEST !!!")

    def _setup_event_detection(self):
        self.screen_provider.add_keystroke_action(self._generate_maze, "g")
        self.screen_provider.add_keystroke_action(
            self.event_processor.higher_speed, "h"
        )
        self.screen_provider.add_keystroke_action(self.event_processor.lower_speed, "l")
        self.screen_provider.add_keystroke_action(self.print_test, "p")
        self.screen_provider.listen_to_keystrokes()
        self.event_processor.process()

    def _get_maze_origo(self, maze_size) -> Point:
        x = -(maze_size / 2) * ELEMENT_SIZE
        y = (maze_size / 2) * ELEMENT_SIZE
        return Point(x, y)

    def _setup_border_walls_and_status_stamps(self, maze_size):
        maze_border = MazeBorder(self.origo, maze_size, self.update_screen)
        maze_border.draw_maze_border_walls()
        self.walls.draw_walls_between_nodes()
        self.status_stamps.draw_status_stamps()

    def _generate_maze(self):
        self._perform_activity(MazeActivity.GENERATE)

    # def on_event(self, event: Event):
    #     print(f"Event: {event.event_type} {event.to_node} {event.from_node}")

    # self.walls.draw_walls_between_nodes()
    # self.walls.remove_wall_between_nodes([5, 6])
    # self.walls.remove_wall_between_nodes([14, 10])
    # self.status_stamps.initialize_status_stamps()
    # self.status_stamps.show_stamp(0)
    # self.status_stamps.show_stamp(1)
    # self.status_stamps.show_stamp(4)
    # self.status_stamps.show_stamp(5)
    # self.status_stamps.show_stamp(6)
    # self.status_stamps.show_stamp(2)
    # self.status_stamps.hide_stamp(2)
