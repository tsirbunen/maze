from src.graphical_ui.maze_activity import MazeActivity
from src.graphical_ui.toolkit import Toolkit

VIEW_SOLVE_MAZE_OPTIONS = [
    "SOLVING THE MAZE",
    "Would you like to view solving the maze with different algorithms?",
    "- press 'E' to see DEAD END FILLER algorithm live",
    "- press 'W' to see WALL FOLLOWER algorithm live",
    "- press 'D' to see DIJKSTRA algorithm live",
    "- press 'Q' to quit the program",
]

GENERAL_SOLVER_INSTRUCTIONS = [
    "- press 'H' for higher (2 X) speed",
    "- press 'L' for lower (1/2 X) speed",
    "- press 'Q' to quit the program",
]

WALL_FOLLOWER = "WALL FOLLOWER algorithm in action..."
DEAD_END_FILLER = "DEAD END FILLER algorithm in action..."
DIJKSTRA = "DIJKSTRA algorithm in action..."


class MazeSolvingHandler:
    """Handles actions related to solving the maze."""

    def __init__(self, toolkit: Toolkit):
        self._perform_activity = toolkit.perform_activity
        self._show_instructions = toolkit.show_instructions
        self._event_processor = toolkit.event_processor
        self._add_on_keystroke_actions = toolkit.add_on_keystroke_actions

    def handle(self):
        """Shows instructions and sets up keystroke detection related to maze solving."""
        self._show_instructions(VIEW_SOLVE_MAZE_OPTIONS)
        actions = [
            (self._solve_maze_wall_follower, "w"),
            (self._solve_maze_dead_end_filler, "e"),
            (self._solve_maze_dijkstra, "d"),
            (self._event_processor.higher_speed, "h"),
            (self._event_processor.lower_speed, "l"),
        ]
        self._add_on_keystroke_actions(actions)

    def _solve_maze_wall_follower(self):
        self._solve_maze(MazeActivity.SOLVE_WALL_FOLLOWER, WALL_FOLLOWER)

    def _solve_maze_dead_end_filler(self):
        self._solve_maze(MazeActivity.SOLVE_DEAD_END_FILLER, DEAD_END_FILLER)

    def _solve_maze_dijkstra(self):
        self._solve_maze(MazeActivity.SOLVE_DIJKSTRA, DIJKSTRA)

    def _solve_maze(self, maze_activity, specific_info):
        print("_event_processor")
        self._event_processor.process()
        self._perform_activity(maze_activity, True)
        self._show_algorithm_instructions(specific_info)

    def _show_algorithm_instructions(self, specific_info):
        self._show_instructions([specific_info, *GENERAL_SOLVER_INSTRUCTIONS])
