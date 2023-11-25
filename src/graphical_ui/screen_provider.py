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
        self.screen = screen

    def update(self):
        """Must be called after changes to maze elements to make them visible on the screen."""
        self.screen.update()

    def add_on_keystroke_actions(self, actions):
        """Sets up listening to several keystrokes to invoke actions."""
        for action, key in actions:
            self.screen.onkey(action, key)
        turtle.listen()  # pylint: disable=no-member

    def set_exit_on_click(self):
        """Prevents the screen from closing prematurely."""
        self.screen.exitonclick()

    def on_timer(self, action, delay):
        """Sets up a timer to perform an action on screen after a delay."""
        self.screen.ontimer(action, delay)

    def quit_program(self):
        """Closes the UI screen."""
        turtle.bye()  # pylint: disable=no-member
