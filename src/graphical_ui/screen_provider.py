import turtle
from turtle import Screen

from .constants import SCREEN_SIZE

BACKGROUND_COLOR = "black"
GAME_TITLE = "maze game"


class ScreenProvider:
    """Opens up the graphical UI where all action happens"""

    def __init__(self) -> None:
        screen = Screen()
        screen.setup(width=SCREEN_SIZE, height=SCREEN_SIZE)
        screen.title(GAME_TITLE)
        screen.bgcolor(BACKGROUND_COLOR)
        screen.tracer(0)
        self._screen = screen

    def update(self):
        """Must be called after changes to maze elements to make them visible on the screen"""
        self._screen.update()

    def add_keystroke_action(self, action, key):
        self._screen.onkey(action, key)
        # turtle.listen()  # pylint: disable=no-member

    def listen_to_keystrokes(self):
        turtle.listen()  # pylint: disable=no-member

    def set_exit_on_click(self):
        """Prevents the screen from closing prematurely"""
        self._screen.exitonclick()

    def on_timer(self, action, delay):
        self._screen.ontimer(action, delay)

    def quit_program(self):
        turtle.bye()
