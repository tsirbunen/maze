import random

# from src.events.event import Event, EventType

from src.maze_parameters.maze_type import MazeType
from .maze_generator_logger import MazeGeneratorLogger
from .basic_maze_operations import BasicMazeOperations


class WallRemover(BasicMazeOperations):
    def __init__(self, parameters, dispatch_event, connections: [[int]]):
        super().__init__(parameters.size)
        self.parameters = parameters
        self.connections = connections
        self.dispatch_event = dispatch_event

    def perform(self):
        if self.parameters.maze_type == MazeType.MULTIPLE:
            print("")
        # self.dispatch_event(Event(EventType.PHASE_COMPLETED, None, None))

    def get_result(self) -> [[int]]:
        return self.connections
