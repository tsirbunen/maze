from src.maze_parameters.maze_parameters import MazeParameters
from src.maze_parameters.maze_type import MazeType
from src.utils.logger import Logger
from .phase import Phase


MAZE_GENERATION_INFO_TITLE = "\n\tMAZE GENERATION:"
MAZE_DETAILS_INFO = "\tGenerate a maze with size SIZE x SIZE and SOLUTIONS."
SINGLE = "a single solution"
MULTIPLE = "multiple solutions"
START_GENERATING = "\tStarted generating the maze using the Twist & Merge algorithm..."
TWISTING_INFO = "\t...working on the TWISTING phase..."
MERGING_INFO = "\t...working on the MERGING phase..."
WALL_REMOVING_INFO = (
    "\t...working on the WALL REMOVAL phase (to enable multiple solutions)..."
)
COMPLETED_INFO = "\t...and completed the job!"


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
        self.logger.log_yellow(message)

    def log_start_generating_maze(self) -> None:
        self.logger.log_pink(MAZE_GENERATION_INFO_TITLE)
        size = self.parameters.size
        solutions = SINGLE if self.parameters.maze_type == MazeType.SINGLE else MULTIPLE
        maze_details = MAZE_DETAILS_INFO.replace("SIZE", f"{size}").replace(
            "SOLUTIONS", solutions
        )
        info = [maze_details, START_GENERATING]
        for i in range(0, len(info)):
            self.logger.log_yellow(info[i])
