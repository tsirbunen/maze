from .input_getter import InputGetter
from .input_validators import validate_maze_size, validate_maze_type
from .maze_parameters import MazeType
from .maze_parameters import MazeParameters
from .constants import SIZE_QUESTION, SIZE_ERROR, TYPE_QUESTION, TYPE_ERROR


class ParametersQuerier:
    def get_parameters(self) -> MazeParameters:
        maze_size = self.get_size()
        maze_type = self.get_type()
        return MazeParameters(maze_size, maze_type)

    # Note: these two methods are not made private so that we can mock them in tests!

    def get_size(self) -> int:
        return int(InputGetter().get_valid_input(SIZE_QUESTION, validate_maze_size, SIZE_ERROR))

    def get_type(self) -> MazeType:
        mazeType = InputGetter().get_valid_input(TYPE_QUESTION, validate_maze_type, TYPE_ERROR)
        return MazeType.SINGLE if mazeType == 's' else MazeType.MULTIPLE









