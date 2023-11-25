from src.graphical_ui.maze_activity import MazeActivity
from src.graphical_ui.toolkit import Toolkit

GENERATE_MAZE_OPTIONS = [
    "MAZE GENERATION",
    "Would you like to view maze generation steps live?",
    "- press 'G' to see live maze generation",
    "- press 'S' to skip live viewing",
    "- press 'Q' to quit the program",
]

GENERATE_MAZE_CONTENT = [
    "TWIST & MERGE GENERATION ALGORITHM",
    "- press 'H' for higher (2 X) speed",
    "- press 'L' for lower (1/2 X) speed",
    "- press 'S' to stop viewing maze generation",
    "- press 'Q' to quit the program",
]


class MazeGenerationHandler:
    """Handles actions related to generation of the maze."""

    def __init__(self, toolkit: Toolkit):
        self._perform_activity = toolkit.perform_activity
        self._show_instructions = toolkit.show_instructions
        self._event_processor = toolkit.event_processor
        self._add_on_keystroke_actions = toolkit.add_on_keystroke_actions

    def handle(self):
        """Shows instructions and sets up keystroke detection related to maze generation."""
        self._show_instructions(GENERATE_MAZE_OPTIONS)
        actions = [
            (self._generate_maze_with_live_viewing, "g"),
            (self._generate_maze_without_live_viewing, "s"),
        ]
        self._add_on_keystroke_actions(actions)

    def _generate_maze_with_live_viewing(self):
        actions = [
            (self._event_processor.higher_speed, "h"),
            (self._event_processor.lower_speed, "l"),
            (self._event_processor.stop_processing, "s"),
        ]
        self._add_on_keystroke_actions(actions)
        self._event_processor.process()
        self._perform_activity(MazeActivity.GENERATE, True)
        self._show_instructions(GENERATE_MAZE_CONTENT)

    def _generate_maze_without_live_viewing(self):
        self._event_processor.hide_live_viewing()
        self._event_processor.process()
        self._perform_activity(MazeActivity.GENERATE, False)
        self._event_processor.stop_processing()
