from src.events.event import Event
from src.events.observer import Observer
from src.events.publisher import Publisher
from src.maze_generation.merger import Merger
from src.maze_generation.twister import Twister
from src.maze_generation.variables_initializer import VariablesInitializer
from src.maze_generation.wall_remover import WallRemover
from .maze_generator_logger import MazeGeneratorLogger
from src.maze_parameters.maze_parameters import MazeParameters
from .phase import Phase


class MazeGenerator(Publisher):
    def __init__(self, parameters: MazeParameters):
        self.__parameters = parameters
        self.__logger = MazeGeneratorLogger(parameters)
        self.__observers: Observer = []
        self.__is_completed = False
        self.__result = None

    def generate(self):
        self.__initialize()
        self.__perform(Phase.TWIST, Twister)
        self.__perform(Phase.MERGE, Merger)
        self.__perform(Phase.WALL_REMOVAL, WallRemover)
        self.__complete_maze_generation()

    def __initialize(self):
        self.__logger.log(Phase.START)
        initializer = VariablesInitializer(self.__parameters.size)
        self.__result = initializer.get_result()
    
    def __perform(self, phase, phase_performer):
        self.__logger.log(phase)
        performer = phase_performer(self.__parameters, self.dispatch_event, self.__result)
        performer.perform()
        self.__result = performer.get_result()

    def __complete_maze_generation(self):
        self.__logger.log(Phase.COMPLETE)
        self.__is_completed = True

    def get_finished_maze(self):
        if self.__is_completed:
            return self.__result
        raise Exception("Maze not completed yet!")

    def attach_observer(self, observer: Observer):
        self.__observers.append(observer)

    def detach_observer(self, observer: Observer):
        self.__observers.remove(observer)

    def dispatch_event(self, event: Event):
        for observer in self.__observers:
            observer.on_event(event)


