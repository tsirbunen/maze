from turtle import Turtle
from src.graphical_ui.constants import ELEMENT_SIZE

from src.graphical_ui.point import Point
from src.graphical_ui.stamp import Stamp
from src.graphical_ui.stamp_mode import StampMode


SHAPE = "circle"
SHAPE_SIZE = 1
PLAYER_COLOR = "orange"
PATH_COLOR = "green yellow"


class Player:
    def __init__(self, maze_size: int, update_screen, on_timer, maze):
        self.maze = maze
        self.is_big = True
        self.end_node = maze_size * maze_size - 1
        # self.size = SHAPE_SIZE
        self.player = None
        self.path = []
        self.maze_size = maze_size
        self.update_screen = update_screen
        self.on_timer = on_timer
        self.origo = self._get_maze_origo(maze_size)
        self.row = 0
        self.column = 0
        self.node_index = 0
        self.x = self.origo.x + ELEMENT_SIZE * 0.5
        self.y = self.origo.y - ELEMENT_SIZE * 0.5
        self.goal = None

    def setup_player(self):
        player = Turtle()
        player.shape(SHAPE)
        player.color(PLAYER_COLOR)
        player.shapesize(SHAPE_SIZE, SHAPE_SIZE)
        player.penup()
        player.showturtle()
        player.goto(self.x, self.y)
        self.player = player
        self.on_timer(self._blink_player, 500)
        self.update_screen()

    def setup_goal(self):
        x = self.origo.x + (self.maze_size - 1 / 2) * ELEMENT_SIZE
        y = self.origo.y - (self.maze_size - 1 / 2) * ELEMENT_SIZE
        self.goal = Stamp(Point(x, y), StampMode.GOAL)
        self.goal.show()
        self.update_screen()

    def _get_maze_origo(self, maze_size) -> Point:
        x = -(maze_size / 2) * ELEMENT_SIZE
        y = (maze_size / 2) * ELEMENT_SIZE
        return Point(x, y)

    def _blink_player(self):
        size = SHAPE_SIZE
        is_goal = self.node_index == self.end_node
        if is_goal:
            self.player.shapesize(size, size)
            self.update_screen()
            return
        if self.is_big:
            size = size / 1.5
            self.is_big = False
        else:
            self.is_big = True
        self.player.shapesize(size, size)
        self.update_screen()
        self.on_timer(self._blink_player, 500)

    def go_up(self):
        self._move_if_allowed(-1, 0)

    def go_down(self):
        self._move_if_allowed(1, 0)

    def go_left(self):
        self._move_if_allowed(0, -1)

    def go_right(self):
        self._move_if_allowed(0, 1)

    def stop_playing(self):
        for stamp in self.path:
            stamp.hide()
        self.player.hideturtle()
        self.goal.hide()
        self.update_screen()

    def _move_if_allowed(self, change_in_row, change_in_column):
        is_goal = self.node_index == self.end_node
        if is_goal:
            return
        new_index = self.node_index + change_in_row * self.maze_size + change_in_column
        if new_index in self.maze[self.node_index]:
            self._move(change_in_row, change_in_column)
            self.node_index = new_index
            self.update_screen()

    def _move(self, change_in_row, change_in_column):
        self.x += change_in_column * ELEMENT_SIZE
        self.y -= change_in_row * ELEMENT_SIZE
        self._create_path_stamp(self.row, self.column)
        self.row += change_in_row
        self.column += change_in_column
        self.player.goto(self.x, self.y)

    def _create_path_stamp(self, row, column):
        x = self.origo.x + (column + 1 / 2) * ELEMENT_SIZE
        y = self.origo.y - (row + 1 / 2) * ELEMENT_SIZE
        stamp = Stamp(Point(x, y), StampMode.PLAYER_PATH)
        stamp.show()
        self.path.append(stamp)
