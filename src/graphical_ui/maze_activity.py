import enum


class MazeActivity(enum.Enum):
    """Activities that need to be performed outside of the graphical UI."""

    GENERATE = 1
    SOLVE_WALL_FOLLOWER = 2
    SOLVE_DEAD_END_FILLER = 3
    SOLVE_DIJKSTRA = 4
