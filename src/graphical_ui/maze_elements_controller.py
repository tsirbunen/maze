from src.graphical_ui.stamp_activity import StampActivity
from .user_instructions import UserInstructions


from .status_stamps import StatusStamps
from .maze_border import MazeBorder
from .maze_walls import MazeWalls
from .point import Point
from .constants import ELEMENT_SIZE
from .screen_provider import ScreenProvider


class MazeElementsController:
    """Holds all visible elements of the maze."""

    def __init__(self, maze_size) -> None:
        self._maze_size = maze_size
        self.screen_provider = ScreenProvider()
        self._origo = self._get_maze_origo()
        self._walls = MazeWalls(self._origo, maze_size, self.update_screen)
        self._status_stamps = StatusStamps(self._origo, maze_size, self.update_screen)
        self._instructions = UserInstructions()
        self._setup_border_walls_and_status_stamps(maze_size)

    def _get_maze_origo(self) -> Point:
        x = -(self._maze_size / 2) * ELEMENT_SIZE
        y = (self._maze_size / 2) * ELEMENT_SIZE
        return Point(x, y)

    def _setup_border_walls_and_status_stamps(self, maze_size):
        maze_border = MazeBorder(self._origo, maze_size, self.update_screen)
        maze_border.draw_maze_border_walls()
        self._walls.draw_walls_between_nodes()
        self._status_stamps.create_status_stamps()

    def update_screen(self):
        self.screen_provider.update()

    def remove_wall_between_nodes(self, nodes, with_blink=True):
        """Removes a wall between two nodes of the maze (optionally with a blink)."""
        self._walls.remove_wall_between_nodes(nodes, with_blink)

    def handle_stamp_action(self, action, params):
        """Handles an action on a status stamp."""
        match action:
            case StampActivity.SHOW_STAMP:
                self._status_stamps.show_stamp(params)
            case StampActivity.HIDE_STAMP:
                self._status_stamps.hide_stamp(params)
            case StampActivity.HIDE_ALL:
                self._status_stamps.hide_all()
            case StampActivity.SHOW_PATH_STAMP:
                self._status_stamps.show_path_node(params)
            case StampActivity.BLINK_STAMP:
                self._status_stamps.blink_stamp(params)
            case _:
                raise ValueError(f"Unknown stamp action: {action}")

    def show_instructions(self, content):
        """Shows instructions on the screen."""
        self._instructions.display_content(content)

    def perform_after_delay(self, action, delay):
        """Sets up a timer to perform an action on screen after a delay."""
        self.screen_provider.on_timer(action, delay)

    def add_on_keystroke_actions(self, actions):
        """Adds actions to be performed on keystrokes."""
        self.screen_provider.add_on_keystroke_actions(
            [*actions, (self.screen_provider.quit_program, "q")]
        )

    def set_exit_on_click(self):
        """Prevents screen from closing prematurely."""
        self.screen_provider.set_exit_on_click()
