import enum


class StampActivity(enum.Enum):
    """Actions available for status stamps."""

    SHOW_STAMP = 1
    HIDE_STAMP = 2
    HIDE_ALL = 3
    SHOW_PATH_STAMP = 4
    BLINK_STAMP = 5
