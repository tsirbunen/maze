import enum


class MazeType(enum.Enum):
    """Describes the number of solutions for the maze: single or multiple."""

    SINGLE = 1
    MULTIPLE = 2
