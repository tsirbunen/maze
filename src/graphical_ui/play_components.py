from math import sqrt
from src.graphical_ui.constants import ELEMENT_SIZE
from src.graphical_ui.goal import Goal
from src.graphical_ui.player import Player
from src.graphical_ui.point import Point
from src.graphical_ui.stamp import Stamp
from src.graphical_ui.stamp_mode import StampMode


SHAPE = "circle"
SHAPE_SIZE = 1
PLAYER_COLOR = "orange"
PATH_COLOR = "green yellow"


class PlayComponents:
    """Shows the movable player stamp, the goal, and the path the player has taken so far."""

    _node_index = 0
    _path = []

    def __init__(self, update_screen, on_timer, maze):
        self._maze = maze
        self._maze_size = int(sqrt(len(maze)))
        self._update_screen = update_screen
        self._origo = self._get_maze_origo(self._maze_size)
        self._goal = Goal(self._origo, self._maze_size)
        self._player = Player(self._origo, self._update_screen, on_timer)

    def start_playing(self):
        """Performs set ups needed to start playing."""
        self._player.play()
        self._goal.play()
        self._update_screen()

    def stop_playing(self):
        """Stops the playing step."""
        for stamp in self._path:
            stamp.hide()
        self._player.hideturtle()
        self._goal.hide()
        self._update_screen()

    def go(self, direction):
        """Moves player one node in the given direction if allowed."""
        match direction:
            case "Up":
                return self._go_up
            case "Down":
                return self._go_down
            case "Left":
                return self._go_left
            case "Right":
                return self._go_right
            case _:
                raise ValueError(f"Unknown direction: {direction}")

    def _go_up(self):
        self._move_if_allowed(-1, 0)

    def _go_down(self):
        self._move_if_allowed(1, 0)

    def _go_left(self):
        self._move_if_allowed(0, -1)

    def _go_right(self):
        self._move_if_allowed(0, 1)

    def _is_already_at_goal(self):
        return self._node_index == self._maze_size * self._maze_size - 1

    def _move_if_allowed(self, change_in_row, change_in_column):
        if self._is_already_at_goal():
            return
        new_index = (
            self._node_index + change_in_row * self._maze_size + change_in_column
        )
        if new_index in self._maze[self._node_index]:
            self._create_path_stamp()
            self._node_index = new_index
            self._move_player()
            self._update_screen()

    def _get_maze_origo(self, maze_size) -> Point:
        x = -(maze_size / 2) * ELEMENT_SIZE
        y = (maze_size / 2) * ELEMENT_SIZE
        return Point(x, y)

    def _get_current_coordinates(self):
        row = int(self._node_index / self._maze_size)
        column = self._node_index % self._maze_size
        x = self._origo.x + (column + 1 / 2) * ELEMENT_SIZE
        y = self._origo.y - (row + 1 / 2) * ELEMENT_SIZE
        return (x, y)

    def _move_player(self):
        (x, y) = self._get_current_coordinates()
        self._player.move_to(x, y)

    def _create_path_stamp(self):
        (x, y) = self._get_current_coordinates()
        stamp = Stamp(Point(x, y), StampMode.PLAYER_PATH)
        stamp.show()
        self._path.append(stamp)
