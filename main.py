from src.events.queue_observer import QueueObserver
from src.events.event_queue import EventQueue
from src.graphical_ui.maze_activity import MazeActivity
from src.maze_parameters.maze_parameters import MazeParameters
from src.maze_parameters.maze_type import MazeType
from src.maze_parameters.parameters_querier import ParametersQuerier
from src.maze_generation.maze_generator import MazeGenerator
from src.graphical_ui.graphical_ui import GraphicalUI
from src.maze_solving.maze_solver import MazeSolver


class MazeProgram:
    """The top-level program that orchestrates cli interactions and displaying the graphical UI."""

    def __init__(self) -> None:
        self.event_queue = EventQueue()
        self.event_observer = QueueObserver(self.event_queue)
        self.graphical_ui = None
        self.maze_generator = None
        self.maze_solver = None
        # self.maze = None

    def run(self):
        """The main entry point of the program."""
        # querier = ParametersQuerier()
        # parameters = querier.get_parameters()
        parameters = MazeParameters(3, MazeType.SINGLE)
        self.maze_generator = MazeGenerator(parameters)
        self.maze_generator.attach_observer(self.event_observer)
        self.graphical_ui = GraphicalUI(
            parameters.size,
            self.event_queue,
            self._perform_activity,
        )

    def _perform_activity(self, activity: MazeActivity, parameters):
        if activity == MazeActivity.GENERATE:
            self._generate_maze(with_event_dispatching=parameters)
            return
        if self.maze_solver is None:
            self._setup_solver()
        if activity == MazeActivity.SOLVE_WALL_FOLLOWER:
            print("Solving with wall follower")
            self.maze_solver.solve_with_wall_follower()
        elif activity == MazeActivity.SOLVE_DEAD_END_FILLER:
            print("Solving with dead end filler")
            self.maze_solver.solve_with_dead_end_filler()
        elif activity == MazeActivity.SOLVE_DIJKSTRA:
            print("Solving with dijkstra")
            self.maze_solver.solve_with_dijkstra()
        else:
            raise ValueError("Unknown activity")

    def _generate_maze(self, with_event_dispatching):
        self.maze_generator.generate(with_event_dispatching)

    def _setup_solver(self):
        maze = self.maze_generator.get_finished_maze()
        self.maze_solver = MazeSolver(maze)
        self.maze_solver.attach_observer(self.event_observer)


maze_program = MazeProgram()
maze_program.run()
