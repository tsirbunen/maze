import time
from src.maze_parameters.maze_parameters import MazeParameters
from src.events.event import Event
from src.events.observer import Observer
from src.events.publisher import Publisher
from .merger import Merger
from .twister import Twister
from .variables_initializer import VariablesInitializer
from .wall_remover import WallRemover
from .maze_generator_logger import MazeGeneratorLogger
from .phase import Phase


class MazeGenerator(Publisher):
    """
    Maze generator orchestrates generating a maze from input parameters of size and maze type.
    Size refers to the maze edge, and maze type refers to the number of solutions the maze
    should have (single or multiple). For generation, a slightly modified version of the
    Twist & Merge algorithm is used. The generated maze is a graph of connections between
    nodes in the maze. Optionally subscribers can be attached to the Maze generator to receive
    information on generation events (such as a connection was created between two nodes).
    """

    def __init__(self, parameters: MazeParameters):
        self._parameters = parameters
        self._logger = MazeGeneratorLogger(parameters)
        self._observers: Observer = []
        self._is_completed = False
        self._result = None

    def generate(self):
        """Generate the maze with the given parameters."""
        self._initialize()
        self._perform(Phase.TWIST, Twister)
        self._perform(Phase.MERGE, Merger)
        self._perform(Phase.WALL_REMOVAL, WallRemover)
        self._complete_maze_generation()

    def _initialize(self):
        self._logger.log(Phase.START)
        initializer = VariablesInitializer(self._parameters.size)
        self._result = initializer.get_result()

    def _perform(self, phase, phase_performer):
        self._logger.log(phase)
        performer = phase_performer(self._parameters, self.dispatch_event, self._result)
        performer.perform()
        self._result = performer.get_result()

    def _complete_maze_generation(self):
        self._logger.log(Phase.COMPLETE)
        self._is_completed = True

    def get_finished_maze(self):
        """Returns the maze as a graph of connections between nodes ([[int]]) if completed."""
        if self._is_completed:
            return self._result
        raise ValueError("Maze not completed yet!")

    def attach_observer(self, observer: Observer):
        self._observers.append(observer)

    def detach_observer(self, observer: Observer):
        self._observers.remove(observer)

    def dispatch_event(self, event: Event):
        # Note: Wait for a little while so that the events enter the queue in the right order
        time.sleep(0.01)
        for observer in self._observers:
            observer.on_event(event)
