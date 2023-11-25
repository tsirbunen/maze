from src.graphical_ui.constants import ELEMENT_SIZE
from src.graphical_ui.point import Point
from src.graphical_ui.stamp import Stamp
from src.graphical_ui.stamp_mode import StampMode


SHAPE = "circle"
SHAPE_SIZE = 1
PLAYER_COLOR = "orange"
PATH_COLOR = "green yellow"


class Goal(Stamp):
    """Shows the goal node as a stamp."""

    def __init__(self, origo, maze_size):
        x = origo.x + (maze_size - 1 / 2) * ELEMENT_SIZE
        y = origo.y - (maze_size - 1 / 2) * ELEMENT_SIZE
        goal_location = Point(x, y)
        super().__init__(goal_location, StampMode.GOAL)
        # self.show()

    def play(self):
        """Makes the goal visible."""
        self.show()
