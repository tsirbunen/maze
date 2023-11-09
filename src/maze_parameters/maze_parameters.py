from dataclasses import dataclass
from .maze_type import MazeType


@dataclass
class MazeParameters:
    """Parameters for maze generation: size (N x N) and type (single or multiple solutions)."""

    size: int
    maze_type: MazeType
