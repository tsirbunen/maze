from .maze_type import MazeType

class MazeParameters:
    def __init__(self, size: int, maze_type: MazeType) -> None:
        self.size = size
        self.maze_type = maze_type
