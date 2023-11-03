# import turtle
from turtle import Screen
from .constants import BACKGROUND_COLOR, SCREEN_SIZE, GAME_TITLE


class ScreenProvider:
    def __init__(self) -> None:
        screen = Screen()
        screen.setup(width=SCREEN_SIZE, height=SCREEN_SIZE)
        screen.title(GAME_TITLE)
        screen.bgcolor(BACKGROUND_COLOR)
        screen.tracer(0)
        self.screen = screen

    def set_exit_on_click(self):
        self.screen.exitonclick()


