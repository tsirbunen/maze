from turtle import Turtle

from .stamp_mode import StampMode
from .point import Point

STAMP_COLORS = {StampMode.TWISTED: "dodger blue"}
SHAPE = "circle"
SHAPE_SIZE = 1


class Stamp(Turtle):
    """Draws a circular stamp inside a maze node; stamp color can be controlled by its mode"""

    def __init__(self, point: Point, mode: StampMode):
        super().__init__()
        self.hideturtle()
        self.shape(SHAPE)
        self.color(self._get_stamp_color_by_mode(mode))
        self.shapesize(SHAPE_SIZE, SHAPE_SIZE)
        self.penup()
        self.goto(point.x, point.y)

    def _get_stamp_color_by_mode(self, mode: StampMode):
        return STAMP_COLORS[mode]

    def show(self):
        """Makes the stamp visible on screen."""
        self.showturtle()

    def hide(self):
        """Makes the stamp invisible on screen (but does not remove it altogether)."""
        self.hideturtle()

    def change_mode(self, mode: StampMode):
        """Changes the mode of the stamp, which leads to the change of its color."""
        self.color(self._get_stamp_color_by_mode(mode))
