from .stamp import Stamp
from .stamp_mode import StampMode
from .constants import ELEMENT_SIZE
from .point import Point


class StatusStamps:
    """Shows the progress of maze algorithms by drawing dots on the screen."""

    def __init__(self, origo: Point, maze_size: int, update_screen):
        self.maze_origo = origo
        self.maze_size = maze_size
        self._update_screen = update_screen
        self.status_stamps = []

    def draw_status_stamps(self):
        """Draws a stamp to each node in the maze; stamps are initially hidden."""
        for row in range(0, self.maze_size):
            for column in range(0, self.maze_size):
                stamp = self._create_stamp_for_one_node(row, column)
                self.status_stamps.append(stamp)
        self._update_screen()

    def _create_stamp_for_one_node(self, row, column):
        x = self.maze_origo.x + (column + 1 / 2) * ELEMENT_SIZE
        y = self.maze_origo.y - (row + 1 / 2) * ELEMENT_SIZE
        return Stamp(Point(x, y), StampMode.TWISTED)

    def show_stamp(self, node):
        """Makes the stamp of a node visible on screen."""
        self.status_stamps[node].show()
        self._update_screen()

    def hide_stamp(self, node):
        """Makes the stamp of a node invisible on screen."""
        self.status_stamps[node].hide()
        self._update_screen()

    def hide_all_stamps(self):
        """Makes the stamp of a node invisible on screen."""
        for stamp in self.status_stamps:
            stamp.hide()
        self._update_screen()

    # def show_in_color(self, node, color):
    #     status_node = self.status_stamps[node]
    #     node.color = color
    #     node.show()
    #     self._update_screen()
