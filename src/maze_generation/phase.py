import enum


class Phase(enum.Enum):
    START = 1
    TWIST = 2
    MERGE = 3
    WALL_REMOVAL = 4
    COMPLETE = 5
