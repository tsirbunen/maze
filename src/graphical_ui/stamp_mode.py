import enum


class StampMode(enum.Enum):
    """Different kind of stamps (=differently colored) that can be shown on the screen."""

    GENERATE_MAZE = 1
    PLAYER_PATH = 2
    GOAL = 3
    SOLUTION_PATH = 4
    BLINK = 5
