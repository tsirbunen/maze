from turtle import Turtle

from src.graphical_ui.constants import ELEMENT_SIZE, SCREEN_SIZE

INSTRUCTIONS_TEXT_COLOR = "gray50"
TITLE_LINE_DIFFERENCE = 50
LINE_DIFFERENCE = 30
TITLE_FONT = ("Arial", 26, "bold")
SMALL_FONT = ("Arial", 20, "normal")
BASE_DISTANCE_FROM_TOP = 65
TEXT_ALIGNMENT = "left"
LEFT_POSITION = -10 * ELEMENT_SIZE
TOP_BASE = SCREEN_SIZE / 2 - BASE_DISTANCE_FROM_TOP


class UserInstructions(Turtle):
    """Responsible for showing instructions for the user in the graphical UI."""

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color(INSTRUCTIONS_TEXT_COLOR)

    def display_content(self, content):
        """Shows text content on the screen (replaces previous content if present)."""
        self._clear_all_instructions_from_screen()
        title, *lines = content
        self._show_title(title)
        for index, line in enumerate(lines):
            self.goto(LEFT_POSITION, TOP_BASE - (index + 1) * LINE_DIFFERENCE)
            self._write_on_screen(line, SMALL_FONT)

    def _show_title(self, title):
        self.goto(LEFT_POSITION, TOP_BASE)
        self._write_on_screen(title, TITLE_FONT)

    def _write_on_screen(self, text, font):
        self.write(text, align=TEXT_ALIGNMENT, font=font)

    def _clear_all_instructions_from_screen(self):
        self.clear()
