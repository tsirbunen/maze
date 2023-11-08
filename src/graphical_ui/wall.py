from turtle import Turtle
from .constants import ELEMENT_SIZE, WALL_COLOR, WALL_WIDTH, BLINK_COLOR
from .point import Point


class Wall(Turtle):
    """Draws a vertical or horizontal wall between two nodes in a maze."""

    def __init__(self, point: Point, angle: int):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(point.x, point.y)
        self.pendown()
        self.color(WALL_COLOR)
        self.width(WALL_WIDTH)
        self.right(angle)
        self.forward(ELEMENT_SIZE)

    def draw_wall_in_blink_color(self):
        """Change wall color so that it appears to blink (on removal)."""
        self.color(BLINK_COLOR)
        self.right(180)
        self.penup()
        self.forward(WALL_WIDTH)
        self.pendown()
        self.forward(ELEMENT_SIZE - WALL_WIDTH * 2)
