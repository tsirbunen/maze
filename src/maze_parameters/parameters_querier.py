from src.utils.logger import Logger
from .input_getter import InputGetter
from .maze_parameters import MazeType
from .maze_parameters import MazeParameters
from .constants import SIZE_QUESTION, SIZE_ERROR, TYPE_QUESTION, TYPE_ERROR
from .constants import MIN_SIZE, MAX_SIZE, WELCOME, INSTRUCTIONS, YOUR_INPUT_TITLE


class ParametersQuerier:
    """Asks the user for the maze parameters (size and type) and returns them."""

    def get_parameters(self) -> MazeParameters:
        """Performs querying the user for the maze parameters and returns them."""
        self._log_instructions()
        maze_size = self._get_size()
        maze_type = self._get_type()
        return MazeParameters(maze_size, maze_type)

    def _log_instructions(self):
        for line in WELCOME:
            Logger.log_pink(line)

        for line_group in INSTRUCTIONS:
            for index, line in enumerate(line_group):
                if index == 0:
                    Logger.log_pink(line)
                else:
                    Logger.log_yellow(line)

        Logger.log_pink(YOUR_INPUT_TITLE)

    def _get_size(self) -> int:
        return int(
            InputGetter().get_valid_input(
                SIZE_QUESTION, self._validate_maze_size, SIZE_ERROR
            )
        )

    def _get_type(self) -> MazeType:
        maze_type = InputGetter().get_valid_input(
            TYPE_QUESTION, self._validate_maze_type, TYPE_ERROR
        )
        return MazeType.SINGLE if maze_type == "s" else MazeType.MULTIPLE

    def _validate_maze_size(self, value: str) -> bool:
        try:
            size = int(value)
            return MIN_SIZE <= size <= MAX_SIZE
        except ValueError:
            return False

    def _validate_maze_type(self, value: str) -> bool:
        return value == "s" or value == "m"
