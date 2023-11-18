import enum
from dataclasses import dataclass


class EventType(enum.Enum):
    """Maze generation or solving algorithms or its phase."""

    MAZE_GENERATION_COMPLETED = 1
    PERMANENT_NODE = 2
    REMOVE_WALL = 3
    TEMPORARY_ROOT = 4
    TEMPORARY_NEIGHBOR = 5
    PHASE_COMPLETED = 6
    SOLVING_COMPLETED = 7


@dataclass
class AlgorithmEvent:
    """Holds information on maze algorithm generation or solving algorithm progress."""

    algorithm_event_type: EventType
    nodes: [int]
