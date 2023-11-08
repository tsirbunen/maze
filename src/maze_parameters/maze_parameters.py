from dataclasses import dataclass
from .maze_type import MazeType

@dataclass
class MazeParameters:
    size: int
    maze_type: MazeType