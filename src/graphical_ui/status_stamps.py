import time
from .stamp import Stamp
from .stamp_mode import StampMode
from .constants import ELEMENT_SIZE
from .point import Point

BLINK_COLOR = "orange"


class StatusStamps:
    """Shows the progress of an algorithm by drawing various dots on the screen."""

    def __init__(self, origo: Point, maze_size: int, update_screen):
        self.maze_origo = origo
        self.maze_size = maze_size
        self._update_screen = update_screen
        self.status_stamps = []

    def create_status_stamps(self):
        """Draws a stamp to each node in the maze; stamps are initially hidden."""
        for row in range(0, self.maze_size):
            for column in range(0, self.maze_size):
                stamp = self._create_stamp_for_one_node(row, column)
                self.status_stamps.append(stamp)
        self._update_screen()

    def _create_stamp_for_one_node(self, row, column):
        x = self.maze_origo.x + (column + 1 / 2) * ELEMENT_SIZE
        y = self.maze_origo.y - (row + 1 / 2) * ELEMENT_SIZE
        return Stamp(Point(x, y), StampMode.GENERATE_MAZE)

    def show_stamp(self, node):
        """Makes the stamp of a node visible on screen."""
        self.status_stamps[node].show()
        self._update_screen()

    def hide_stamp(self, node):
        """Makes the stamp of a node invisible on screen."""
        self.status_stamps[node].hide()
        self._update_screen()

    def hide_all(self):
        """Makes the stamp of a node invisible on screen."""
        for stamp in self.status_stamps:
            stamp.hide()
        self._update_screen()

    def show_path_node(self, node):
        """Shows a node of a solution path."""
        stamp = self.status_stamps[node]
        stamp.show()
        stamp.change_mode(StampMode.SOLUTION_PATH)
        self._update_screen()

    def blink_stamp(self, node):
        """Makes the stamp blink on screen."""
        stamp = self.status_stamps[node]
        stamp.show()
        stamp.change_mode(StampMode.BLINK)
        self._update_screen()
        time.sleep(0.5)
        stamp.change_mode(StampMode.GENERATE_MAZE)
        stamp.hide()
        self._update_screen()
