from src.maze_parameters.maze_parameters import MazeParameters
from src.maze_parameters.maze_type import MazeType
from src.utils.logger import Logger
from .constants import MAZE_GENERATION_INFO_TITLE, START_GENERATING, MAZE_DETAILS_INFO, SINGLE, MULTIPLE
from .constants import TWISTING_INFO, MERGING_INFO, WALL_REMOVING_INFO, COMPLETED_INFO
from .phase import Phase



class MazeGeneratorLogger:
    def __init__(self, parameters: MazeParameters) -> None:
        self.parameters = parameters
        self.logger = Logger()

    def log(self, info: Phase) -> None:
        message = ""
        match info:
            case Phase.START:
                self.log_start_generating_maze()
                return
            case Phase.TWIST:
                message = TWISTING_INFO
            case Phase.MERGE:
                message = MERGING_INFO
            case Phase.WALL_REMOVAL:
                message = WALL_REMOVING_INFO
            case Phase.COMPLETE:
                message = COMPLETED_INFO
            case _:
                raise Exception("Not implemented!")
        self.logger.logYellow(message)


    def log_start_generating_maze(self) -> None:
        self.logger.logPink(MAZE_GENERATION_INFO_TITLE)
        size = self.parameters.size
        solutions = SINGLE if self.parameters.maze_type == MazeType.SINGLE else MULTIPLE
        maze_details = MAZE_DETAILS_INFO.replace("SIZE", f"{size}").replace("SOLUTIONS", solutions)
        info = [maze_details, START_GENERATING]
        for i in range(0, len(info)):
            self.logger.logYellow(info[i])
    




