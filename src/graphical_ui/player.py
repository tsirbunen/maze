from turtle import Turtle
from src.graphical_ui.constants import ELEMENT_SIZE


SHAPE = "circle"
SHAPE_SIZE = 1
PLAYER_COLOR = "orange"
PATH_COLOR = "green yellow"


class Player(Turtle):
    """Shows the movable player stamp."""

    def __init__(self, origo, update_screen, on_timer):
        super().__init__()
        x = origo.x + ELEMENT_SIZE * 0.5
        y = origo.y - ELEMENT_SIZE * 0.5
        self.hideturtle()
        self.shape(SHAPE)
        self.color(PLAYER_COLOR)
        self.shapesize(SHAPE_SIZE, SHAPE_SIZE)
        self.penup()
        self.goto(x, y)
        self.on_timer = on_timer
        self.is_big = True
        self.update_screen = update_screen

    def play(self):
        """Make the player visible to enable playing."""
        self.showturtle()
        self.on_timer(self._blink_player, 500)

    def _blink_player(self):
        size = SHAPE_SIZE
        if self.is_big:
            size = size / 1.5
            self.is_big = False
        else:
            self.is_big = True
        self.shapesize(size, size)
        self.update_screen()
        self.on_timer(self._blink_player, 500)

    def move_to(self, x, y):
        """Moves the player to the given coordinates on the screen."""
        self.goto(x, y)
