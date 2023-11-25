import time
import copy
from src.events.event import AlgorithmEvent, EventType
from src.events.observer import Observer
from src.events.publisher import Publisher


from src.maze_solving.dead_end_filler import DeadEndFiller
from src.maze_solving.dijkstra import Dijkstra
from src.maze_solving.wall_follower import WallFollower


class MazeSolver(Publisher):
    """
    Maze solver orchestrates solving a maze with different algorithms.
    Depending on the algorithm, different kind of events are dispatched
    and those can then, for example, be viewed in the graphical UI.
    """

    def __init__(self, maze: [[int]]):
        self.maze = maze
        self._observers: Observer = []
        self._is_completed = False

    def solve_with_wall_follower(self):
        """Performs solving the maze using the Wall Follower algorithm."""
        self._solve(WallFollower)

    def solve_with_dead_end_filler(self):
        """Performs solving the maze using the Dead End Filler algorithm."""
        self._solve(DeadEndFiller)

    def solve_with_dijkstra(self):
        """Performs solving the maze using the Dijkstra algorithm."""
        self._solve(Dijkstra)

    def _solve(self, selected_solver):
        maze_copy = self._copy_maze()
        solver = selected_solver(maze_copy, self.dispatch_event)
        solver.solve()

    def _copy_maze(self):
        return copy.deepcopy(self.maze)

    def attach_observer(self, observer: Observer):
        self._observers.append(observer)

    def detach_observer(self, observer: Observer):
        self._observers.remove(observer)

    def dispatch_event(self, event: AlgorithmEvent):
        # Note: Wait for a little while so that the events enter the queue in the right order.
        time.sleep(0.001)
        for observer in self._observers:
            observer.on_event(event)
