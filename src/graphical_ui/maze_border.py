from turtle import Turtle
from .constants import WALL_COLOR, WALL_WIDTH, ELEMENT_SIZE
from .point import Point


class MazeBorder:
    """MazeBorder draws a border around the maze (=outer the walls of nodes on the edge)."""

    def __init__(self, origo: Point, maze_size: int, update_screen):
        self.maze_origo = origo
        self.maze_size = maze_size
        self.__update_screen = update_screen
        self.border_drawer = Turtle()
        self.walls_of_all_nodes = []

    def draw_maze_border_walls(self):
        """Draws the maze outer border on screen."""
        self.__prepare_border_drawer()
        self.__move_border_drawer_to_maze_origo()
        self.__draw_all_four_border_lines()
        self.__update_screen()

    def __prepare_border_drawer(self):
        self.border_drawer.hideturtle()
        self.border_drawer.color(WALL_COLOR)
        self.border_drawer.width(WALL_WIDTH)

    def __move_border_drawer_to_maze_origo(self):
        self.border_drawer.penup()
        self.border_drawer.goto(self.maze_origo.x, self.maze_origo.y)
        self.border_drawer.pendown()

    def __draw_all_four_border_lines(self):
        maze_width = self.maze_size * ELEMENT_SIZE
        for _ in range(0, 4):
            self.border_drawer.forward(maze_width)
            self.border_drawer.right(90)
