from .maze_type import MazeType

class MazeParameters:
    def __init__(self, size: int, mazeType: MazeType) -> None:
        self.size = size
        self.mazeType = mazeType
