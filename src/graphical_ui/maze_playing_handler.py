from src.graphical_ui.play_components import PlayComponents
from src.graphical_ui.toolkit import Toolkit

PLAY_MAZE_OPTIONS = [
    "PLAYING THE MAZE",
    "Would you like to try playing?",
    "- press 'Y' to play the maze",
    "- press 'N' to skip playing",
    "- press 'Q' to quit the program",
]

PLAY_MAZE_CONTENT = [
    "PLAYING THE MAZE",
    "- use arrows to move around the maze",
    "- press 'S' to stop playing",
    "- press 'V' to view solving maze",
    "- press 'Q' to quit the program",
]


class MazePlayingHandler:
    """Handles actions related to playing the maze."""

    def __init__(self, toolkit: Toolkit):
        self._perform_activity = toolkit.perform_activity
        self._show_instructions = toolkit.show_instructions
        self._perform_next_step = toolkit.perform_next_step
        self._add_on_keystroke_actions = toolkit.add_on_keystroke_actions
        self.play_components = PlayComponents(
            toolkit.update_screen, toolkit.on_timer, toolkit.maze
        )

    def handle(self):
        """Shows instructions and sets up keystroke detection related to playing the maze."""
        self._show_instructions(PLAY_MAZE_OPTIONS)
        actions = [
            (self._play, "y"),
            (self._skip_playing, "n"),
        ]
        self._add_on_keystroke_actions(actions)

    def _skip_playing(self):
        self._perform_next_step()

    def _move_on_to_view_solving_maze(self):
        self.play_components.stop_playing()
        self._perform_next_step()

    def _play(self):
        self.play_components.start_playing()
        actions = [
            (self.play_components.go("Up"), "Up"),
            (self.play_components.go("Down"), "Down"),
            (self.play_components.go("Left"), "Left"),
            (self.play_components.go("Right"), "Right"),
            (self._move_on_to_view_solving_maze, "s"),
            (self._move_on_to_view_solving_maze, "v"),
        ]
        self._add_on_keystroke_actions(actions)
        self._show_instructions(PLAY_MAZE_CONTENT)
