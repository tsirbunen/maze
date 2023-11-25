import enum


class Phase(enum.Enum):
    """Phases in Twist & Merge maze generation algorithm."""

    START = 1
    TWIST = 2
    MERGE = 3
    WALL_REMOVAL = 4
    COMPLETE = 5
