import enum
from dataclasses import dataclass


class EventType(enum.Enum):
    """The kinds of events that maze generation and solving algorithms can produce"""

    PHASE_COMPLETED = 1
    TWIST = 2
    MERGE_FOCUS = 3
    MERGE_CONNECT = 4
    # MERGE_RELABEL = 5


# from .maze_type import MazeType

# @dataclass
# class MazeParameters:
#     size: int
#     maze_type: MazeType


@dataclass
class Event:
    """Event holds information about the type of the event and the nodes involved in the event"""

    event_type: EventType
    from_node: int
    to_node: int


# @dataclass
# class TwistEvent(Event):
#     event_type: EventType
#     to_node: int
#     from_node: int

#     # def __init__(self, to_node: int, from_node: int):
#     #     super().__init__(EventType.TWIST)
#     #     self.to_node = to_node
#     #     self.from_node = from_node


# class MergeEvent(Event):
#     def __init__(self, to_node: int, from_node: int, event_type: EventType):
#         super().__init__(event_type)
#         self.to_node = to_node
#         self.from_node = from_node
