from .maze_parameters import MazeType
from .maze_parameters import MazeParameters
from .logger import Logger
from .constants import WELCOME, INSTRUCTIONS
from .constants import SIZE_QUESTION, SIZE_ERROR, TYPE_QUESTION, TYPE_ERROR
from .constants import MIN_SIZE, MAX_SIZE

class ParametersQuerier:

    def __init__(self) -> None:
        self.logger = Logger()

    def log_instructions(self):
        for line in WELCOME:
            self.logger.logPink(line)
        for line_group in INSTRUCTIONS:
            for line in range(len(line_group)):
                to_print = line_group[line]
                if line == 0:
                    self.logger.logPink(to_print)
                else:
                    self.logger.logYellow(to_print)


    def get_parameters(self) -> MazeParameters:
        maze_size = self.get_size()
        maze_type = self.get_type()
        return MazeParameters(maze_size, maze_type)
        

    def get_size(self) -> int:
        return int(self.get_parameter(SIZE_QUESTION, self.is_valid_size, SIZE_ERROR))
    

    def get_type(self) -> MazeType:
        mazeType = self.get_parameter(TYPE_QUESTION, self.is_valid_type, TYPE_ERROR)
        return MazeType.SINGLE if mazeType == 's' else MazeType.MULTIPLE


    def get_parameter(self, question, is_valid_fn, error) -> str:
        while True:
            answer = self.get_input(question)
            if is_valid_fn(answer):
                return answer
            self.logger.logYellow(error)


    def get_input(self, question):
        return input(f"\033[94m\t{question}\033[00m")


    def is_valid_size(self, answer) -> bool:
        try:
            size = int(answer)
            return MIN_SIZE <= size <= MAX_SIZE
        except ValueError:
            return False


    def is_valid_type(self, answer) -> bool:
        return answer == 's' or answer == 'm'
