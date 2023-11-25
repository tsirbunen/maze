import enum
from dataclasses import dataclass


class EventType(enum.Enum):
    """Type of event related to maze generation, maze solving algorithm, or its phase."""

    MAZE_GENERATION_COMPLETED = 1
    PERMANENT_NODE = 2
    REMOVE_WALL = 3
    TEMPORARY_ROOT = 4
    TEMPORARY_NEIGHBOR = 5
    PHASE_COMPLETED = 6
    SOLVING_COMPLETED = 7
    PATH_NODE = 8
    BLINK_NODE = 9


@dataclass
class AlgorithmEvent:
    """Type of event and nodes related to the event of maze generation or solving."""

    algorithm_event_type: EventType
    nodes: [int]
