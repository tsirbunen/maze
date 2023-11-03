import enum



class EventType(enum.Enum):
    TWIST = 1
    MERGE_FOCUS = 2
    MERGE_CONNECT = 3
    MERGE_RELABEL = 4


class Event:
    def __init__(self,event_type: EventType):
        self.event_type = event_type

class TwistEvent(Event):
    def __init__(self,to_node: int, from_node: int):
        super().__init__(EventType.TWIST)
        self.to_node = to_node
        self.from_node = from_node

class MergeEvent(Event):
    def __init__(self, to_node: int, from_node: int, event_type: EventType):
        super().__init__(event_type)
        self.to_node = to_node
        self.from_node = from_node

