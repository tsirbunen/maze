import enum


class MazeType(enum.Enum):
    """Describes the number of solutions a maze can have: single or multiple."""

    SINGLE = 1
    MULTIPLE = 2
